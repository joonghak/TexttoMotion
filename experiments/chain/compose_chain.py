#!/home/jong/isaaclab/.venv/bin/python
"""A chain of actions ("달리다가 점프해") as one reference clip: the action clips one after another, joined by blends.

Usage on this computer:
    ./experiments/chain/compose_chain.py run_jump run:2.4 jump:3.54          # clip:seconds, in order
    ./experiments/chain/compose_chain.py walk_run walk:3 run:3 --blend 0.6

Each segment plays its MimicKit clip from its start for the given seconds; a looping clip (walk, run, jump, spinkick)
repeats with its position carried over, as MimicKit's WRAP mode does, a non-looping one (kick) holds its last frame.
At every junction the next segment is turned and moved so that its first frame stands where and how the chain stood
`blend` seconds before the junction, and over those seconds the two are mixed with a smooth weight (3w^2 - 2w^3):
the root's ground velocities (integrated, so the speed changes smoothly from one segment's to the other's), the root
height linearly, root and joint rotations by slerp. After the blend the chain continues as the next segment.
The clips themselves are not edited. Writes MimicKit/data/motions/humanoid/humanoid_chain_<name>.pkl (CLAMP, 60 fps:
an episode ends with the chain), so run_style_walk.py can train it as the clip "chain_<name>", and
experiments/chain/<name>_strip.png, side views of the chain every 0.2 s with the root speed and the lowest foot
height over time, for a look before training.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MIMICKIT = ROOT / "MimicKit"
sys.path.insert(0, str(MIMICKIT / "mimickit"))
CLIP_DIR = MIMICKIT / "data" / "motions" / "humanoid"
FPS = 60.0


def load_kin():
    import anim.mjcf_char_model as mjcf_char_model

    kin = mjcf_char_model.MJCFCharModel("cpu")
    kin.load(str(MIMICKIT / "data" / "assets" / "humanoid" / "humanoid.xml"))
    return kin


def sample_clip(kin, clip: str, seconds: float):
    """root_pos [T, 3], root_rot [T, 4], joint_rot [T, J, 4] of a clip played from its start for seconds at FPS."""
    import torch

    import anim.motion_lib as motion_lib
    import util.torch_util as torch_util

    lib = motion_lib.MotionLib(str(CLIP_DIR / f"humanoid_{clip}.pkl"), kin, "cpu")
    times = torch.arange(int(round(seconds * FPS)) + 1, dtype=torch.float32) / FPS
    ids = torch.zeros_like(times, dtype=torch.long)
    root_pos, root_rot, _, _, joint_rot, _ = lib.calc_motion_frame(ids, times)
    bad = ~torch.isfinite(joint_rot).all(dim=-1)  # the walk clip's neck is NaN, which MimicKit reads as identity
    joint_rot[bad] = torch.tensor([0.0, 0.0, 0.0, 1.0])
    return root_pos.clone(), torch_util.quat_pos(root_rot).clone(), torch_util.quat_pos(joint_rot).clone()


def yaw_quat(angle):
    import torch

    angle = torch.as_tensor(angle, dtype=torch.float32)
    return torch.stack([torch.zeros_like(angle), torch.zeros_like(angle), torch.sin(angle / 2), torch.cos(angle / 2)], -1)


def place(segment, at_pos, at_rot):
    """The segment turned about the vertical and moved so that its first frame has the heading of at_rot and the
    ground position of at_pos (heights are kept)."""
    import torch

    import util.torch_util as torch_util

    root_pos, root_rot, joint_rot = segment
    turn = torch_util.calc_heading(at_rot.unsqueeze(0))[0] - torch_util.calc_heading(root_rot[:1])[0]
    q = yaw_quat(turn).expand(root_rot.shape)
    rel = root_pos - root_pos[:1]
    rel[:, 2] = 0.0
    moved = torch_util.quat_rotate(q, rel)
    new_pos = moved + torch.tensor([at_pos[0], at_pos[1], 0.0])
    new_pos[:, 2] = root_pos[:, 2]
    return new_pos, torch_util.quat_mul(q, root_rot), joint_rot


def compose(kin, segments: list, blend_s: float):
    import torch

    import util.torch_util as torch_util

    pos, rot, joints = sample_clip(kin, *segments[0])
    blend_n = int(round(blend_s * FPS))
    junctions = []
    for clip, seconds in segments[1:]:
        start = len(pos) - 1 - blend_n  # the blend covers the last blend_n frames of the chain so far
        nxt = place(sample_clip(kin, clip, seconds + blend_s), pos[start], rot[start])
        u = torch.arange(blend_n + 1, dtype=torch.float32) / max(blend_n, 1)
        w = 3 * u ** 2 - 2 * u ** 3
        # ground velocities mixed and integrated (mixing the positions themselves stalls the root mid-blend when the
        # two segments move at different speeds); heights mixed directly
        vel_a = torch.diff(pos[start:, :2], dim=0)
        vel_b = torch.diff(nxt[0][:blend_n + 1, :2], dim=0)
        mid = 0.5 * (w[1:] + w[:-1])[:, None]
        steps = (1 - mid) * vel_a + mid * vel_b
        mixed_pos = (1 - w[:, None]) * pos[start:] + w[:, None] * nxt[0][:blend_n + 1]
        mixed_pos[:, :2] = pos[start, :2] + torch.cat([torch.zeros(1, 2), torch.cumsum(steps, dim=0)])
        shift = mixed_pos[-1, :2] - nxt[0][blend_n, :2]
        nxt = (nxt[0].clone(), nxt[1], nxt[2])
        nxt[0][:, :2] += shift
        mixed_rot = torch_util.slerp(rot[start:], nxt[1][:blend_n + 1], w)
        mixed_joints = torch_util.slerp(joints[start:], nxt[2][:blend_n + 1], w[:, None])
        pos = torch.cat([pos[:start], mixed_pos, nxt[0][blend_n + 1:]])
        rot = torch.cat([rot[:start], mixed_rot, nxt[1][blend_n + 1:]])
        joints = torch.cat([joints[:start], mixed_joints, nxt[2][blend_n + 1:]])
        junctions.append((start / FPS, (start + blend_n) / FPS))
    return pos, torch_util.quat_pos(rot), torch_util.quat_pos(joints), junctions


def save(kin, name: str, pos, rot, joints) -> Path:
    import anim.motion as motion
    import util.torch_util as torch_util

    dof = kin.rot_to_dof(joints)
    frames = np.concatenate([pos.numpy(), torch_util.quat_to_exp_map(rot).numpy(), dof.numpy()], axis=-1)
    out = CLIP_DIR / f"humanoid_chain_{name}.pkl"
    motion.Motion(loop_mode=motion.LoopMode.CLAMP, fps=FPS, frames=frames.astype(np.float32)).save(str(out))
    return out


def strip(kin, name: str, pos, rot, joints, junctions, title: str) -> Path:
    """Side views every 0.2 s (x forward, z up), root speed and lowest foot height over time."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import torch

    body_pos, body_rot = kin.forward_kinematics(pos, rot, joints)
    names = kin.get_body_names()
    sys.path.insert(0, str(ROOT / "experiments" / "t2m_compare"))
    import measure as ms

    lowest = ms.sim_lowest(body_pos.numpy().astype(np.float64), body_rot.numpy().astype(np.float64), list(names))
    bp = body_pos.numpy()
    parents = [kin.get_parent_id(j) for j in range(len(names))]
    t = np.arange(len(bp)) / FPS
    speed = np.linalg.norm(np.gradient(pos[:, :2].numpy(), 1.0 / FPS, axis=0), axis=-1)
    fig = plt.figure(figsize=(16, 7))
    ax = fig.add_subplot(2, 1, 1)
    for k in range(0, len(bp), int(0.2 * FPS)):
        colour = "tab:red" if any(a <= t[k] <= b for a, b in junctions) else "tab:blue"
        for j, p in enumerate(parents):
            if p >= 0:
                ax.plot([bp[k, p, 0], bp[k, j, 0]], [bp[k, p, 2], bp[k, j, 2]], color=colour, lw=1)
    ax.axhline(0.0, color="k", lw=0.5)
    ax.set_aspect("equal")
    ax.set_title(f"{title}: side views every 0.2 s (red: inside a blend)")
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(t, speed, label="root speed (m/s)")
    ax2.plot(t, lowest * 100, label="lowest foot point (cm)")
    for a, b in junctions:
        ax2.axvspan(a, b, color="tab:red", alpha=0.15)
    ax2.set_xlabel("time (s)")
    ax2.legend()
    out = HERE / f"{name}_strip.png"
    fig.tight_layout()
    fig.savefig(out, dpi=80)
    return out


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("name")
    cli.add_argument("segments", nargs="+", help="clip:seconds, e.g. run:2.4")
    cli.add_argument("--blend", type=float, default=0.5, help="blend seconds at each junction (default 0.5)")
    args = cli.parse_args()
    segments = [(s.split(":")[0], float(s.split(":")[1])) for s in args.segments]
    kin = load_kin()
    pos, rot, joints, junctions = compose(kin, segments, args.blend)
    out = save(kin, args.name, pos, rot, joints)
    png = strip(kin, args.name, pos, rot, joints, junctions, " -> ".join(f"{c} {s:g} s" for c, s in segments))
    info = {"name": args.name, "segments": segments, "blend_s": args.blend, "seconds": (len(pos) - 1) / FPS,
            "junctions_s": junctions, "file": str(out), "strip": str(png)}
    (HERE / f"{args.name}.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
