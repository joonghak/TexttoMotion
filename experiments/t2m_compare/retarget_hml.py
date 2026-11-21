#!/home/jong/isaaclab/.venv/bin/python
"""Joint positions of a text-to-motion model (HumanML3D, 22 SMPL joints, 20 fps) moved onto our humanoid, for filming
them next to our policies with the same character and camera (not for the measurements, which use the positions).

Only positions exist, so every body's orientation is built from them: the pelvis from the hips and the spine, the
torso from the shoulders and the spine, the head from neck to head; an upper arm or thigh from its bone and the plane
in which the elbow or knee bends (our elbows and knees are one-axis hinges in that plane), falling back to the trunk's
forward direction when the limb is straight; the forearm and shin from their bone about the same hinge; the foot from
the ankle-to-toe line, taking the median slope of that line while the foot is planted as flat. Local joint rotations
follow from the parents' (our T-pose frames are aligned with the world, as in retarget_100style.py). The path is
scaled by the ratio of leg lengths, resampled to 30 Hz, and lowered by one constant for the whole clip so that the
feet's lowest point over the clip is on the floor: floating, sinking and sliding of the source stay visible.

Check: ./experiments/t2m_compare/retarget_hml.py <joints.npy> prints the mean distance between the source joints
(scaled) and the same points of the retargeted character.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "style_eval"))

import measure as ms  # noqa: E402

OUR_LEG = 0.421546 + 0.409870
FOOT_BOX = ms.FOOT_BOX
J = {"pelvis": 0, "l_hip": 1, "r_hip": 2, "spine1": 3, "l_knee": 4, "r_knee": 5, "spine2": 6, "l_ankle": 7,
     "r_ankle": 8, "spine3": 9, "l_foot": 10, "r_foot": 11, "neck": 12, "l_collar": 13, "r_collar": 14, "head": 15,
     "l_shoulder": 16, "r_shoulder": 17, "l_elbow": 18, "r_elbow": 19, "l_wrist": 20, "r_wrist": 21}


def _norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9)


def _perp(v, axis):
    """Part of v orthogonal to the unit vectors axis."""
    return v - np.sum(v * axis, axis=-1, keepdims=True) * axis


def _frame(x, y, z):
    return np.stack([x, y, z], axis=-1)  # [T, 3, 3], columns are the body axes in the world


def _bend_axis(bone, next_bone, fallback, sign):
    """Unit vector orthogonal to bone toward which next_bone bends (times sign); fallback when nearly straight."""
    bend = _perp(next_bone, bone)
    size = np.linalg.norm(bend, axis=-1, keepdims=True) / np.maximum(np.linalg.norm(next_bone, axis=-1, keepdims=True), 1e-9)
    w = np.clip(size / 0.25, 0.0, 1.0)  # fully trusted from about 15 degrees of bend
    fb = _norm(_perp(fallback, bone))
    return _norm(w * sign * _norm(bend) + (1.0 - w) * fb)


def body_frames(p: np.ndarray) -> dict:
    """Global rotation matrices [T, 3, 3] of our 15 bodies from z-up HumanML3D joints p [T, 22, 3]."""
    g = lambda name: p[:, J[name]]  # noqa: E731
    up = np.array([0.0, 0.0, 1.0])
    f = {}
    y = _norm(g("l_hip") - g("r_hip"))
    z = _norm(_perp(g("spine1") - g("pelvis"), y))
    f["pelvis"] = _frame(np.cross(y, z), y, z)
    y = _norm(g("l_shoulder") - g("r_shoulder"))
    z = _norm(_perp(g("neck") - g("spine1"), y))
    f["torso"] = _frame(np.cross(y, z), y, z)
    z = _norm(g("head") - g("neck"))
    y = _norm(_perp(f["torso"][..., 1], z))
    f["head"] = _frame(np.cross(y, z), y, z)
    trunk_fwd = f["torso"][..., 0]
    for side, s in (("right", "r"), ("left", "l")):
        bone = g(s + "_elbow") - g(s + "_shoulder")
        fore = g(s + "_wrist") - g(s + "_elbow")
        yb = -_norm(bone) if side == "right" else _norm(bone)
        x = _bend_axis(_norm(bone), fore, trunk_fwd - 0.3 * up, 1.0)
        z = _norm(np.cross(x, yb))
        x = np.cross(yb, z)
        f[side + "_upper_arm"] = _frame(x, yb, z)
        yl = -_norm(fore) if side == "right" else _norm(fore)
        zl = _norm(_perp(z, yl))
        f[side + "_lower_arm"] = _frame(np.cross(yl, zl), yl, zl)
        f[side + "_hand"] = f[side + "_lower_arm"]
        thigh = g(s + "_knee") - g(s + "_hip")
        shin = g(s + "_ankle") - g(s + "_knee")
        zt = -_norm(thigh)
        x = _bend_axis(_norm(thigh), shin, f["pelvis"][..., 0], -1.0)  # the shin folds backward
        yt = _norm(np.cross(zt, x))
        f[side + "_thigh"] = _frame(np.cross(yt, zt), yt, zt)
        zs = -_norm(shin)
        ys = _norm(_perp(yt, zs))
        f[side + "_shin"] = _frame(np.cross(ys, zs), ys, zs)
    return f


def foot_frames(p: np.ndarray, frames: dict) -> None:
    """Feet: the ankle-to-toe line turned up by its median slope while planted (flat), lateral axis from the shin."""
    for side, s in (("right", "r"), ("left", "l")):
        line = p[:, J[s + "_foot"]] - p[:, J[s + "_ankle"]]
        slope = np.degrees(np.arctan2(-line[:, 2], np.linalg.norm(line[:, :2], axis=-1)))
        planted = p[:, J[s + "_foot"], 2] < np.percentile(p[:, J[s + "_foot"], 2], 30)
        flat = np.median(slope[planted]) if planted.any() else 20.0
        ys = frames[side + "_shin"][..., 1]
        x = _norm(_perp(line, ys))
        # turn x up about ys by the flat slope
        a = np.radians(flat)
        x = _norm(x * np.cos(a) + np.cross(ys, x) * np.sin(a) * -1.0)
        y = _norm(_perp(ys, x))
        frames[side + "_foot"] = _frame(x, y, np.cross(x, y))


def resample(p: np.ndarray, fps_in: float, fps_out: float) -> np.ndarray:
    t_in = np.arange(len(p)) / fps_in
    t_out = np.arange(int(t_in[-1] * fps_out) + 1) / fps_out
    flat = p.reshape(len(p), -1)
    out = np.stack([np.interp(t_out, t_in, flat[:, k]) for k in range(flat.shape[1])], axis=1)
    return out.reshape((len(t_out),) + p.shape[1:])


def retarget(joints: np.ndarray, kin, device: str = "cpu", fps_in: float = 20.0, fps_out: float = 30.0,
             align: bool = False, align_s: float | None = None):
    """root_pos [T, 3], root_rot [T, 4] (x, y, z, w), joint_rot [T, J-1, 4], dof [T, D] at fps_out; and the scale.
    align turns the whole clip about the vertical so that fixed side and front cameras see every clip from its side and
    its front, as our policies face and walk along +x (a rigid turn: the motion itself is unchanged). The turn puts the
    body's mean facing (hips and shoulders) over the first align_s seconds (the part a video shows; all of it if None)
    along +x; when that facing is not steady (a spin, a circle: the mean of the unit facings is shorter than 0.5) the
    net travel from first to last frame is put along +x instead, and a clip that hardly moves keeps its facing.
    (Until 2026-11-18 the travel alone was used; a clip that walked sideways or crabbed was then filmed 30-80 deg off.)"""
    import torch
    from scipy.spatial.transform import Rotation

    p = np.asarray(joints, dtype=np.float64)[..., [2, 0, 1]]  # y-up (facing +z) -> z-up (facing +x)
    if align:
        shown = p[: int(round(align_s * fps_in))] if align_s else p
        across = shown[:, J["r_hip"]] - shown[:, J["l_hip"]] + shown[:, J["r_shoulder"]] - shown[:, J["l_shoulder"]]
        facing = np.cross([0.0, 0.0, 1.0], across)[:, :2]
        facing = (facing / np.linalg.norm(facing, axis=1, keepdims=True)).mean(axis=0)
        travel = p[-1, J["pelvis"], :2] - p[0, J["pelvis"], :2]
        angle = None
        if np.linalg.norm(facing) >= 0.5:
            angle = -np.arctan2(facing[1], facing[0])
        elif np.linalg.norm(travel) > 0.3:  # a clip that hardly moves keeps its facing
            angle = -np.arctan2(travel[1], travel[0])
        if angle is not None:
            c, s_ = np.cos(angle), np.sin(angle)
            p = p.copy()
            p[..., 0], p[..., 1] = c * p[..., 0] - s_ * p[..., 1], s_ * p[..., 0] + c * p[..., 1]
    leg = np.mean([np.linalg.norm(p[:, J[s + "_hip"]] - p[:, J[s + "_knee"]], axis=-1).mean()
                   + np.linalg.norm(p[:, J[s + "_knee"]] - p[:, J[s + "_ankle"]], axis=-1).mean() for s in "lr"])
    scale = OUR_LEG / leg
    p = resample(p * scale, fps_in, fps_out)
    frames = body_frames(p)
    foot_frames(p, frames)
    names = kin.get_body_names()
    rots = {b: Rotation.from_matrix(frames[b]) for b in names}
    joint_rot = np.stack([(rots[names[kin.get_parent_id(j)]].inv() * rots[names[j]]).as_quat()
                          for j in range(1, len(names))], axis=1)
    root_pos = p[:, J["pelvis"]].copy()
    root_pos[:, :2] -= root_pos[0, :2]
    t = lambda a: torch.tensor(a, dtype=torch.float32, device=device)  # noqa: E731
    joint_rot, root_rot, root_pos = t(joint_rot), t(rots["pelvis"].as_quat()), t(root_pos)
    dof = kin.rot_to_dof(joint_rot)
    joint_rot = kin.dof_to_rot(dof)
    body_pos, body_rot = kin.forward_kinematics(root_pos, root_rot, joint_rot)
    low = ms.sim_lowest(body_pos.cpu().numpy().astype(np.float64), body_rot.cpu().numpy().astype(np.float64), list(names))
    root_pos[:, 2] -= float(np.percentile(low, 2))  # one constant: the clip's own floating and sinking stay
    return {"root_pos": root_pos, "root_rot": root_rot, "joint_rot": joint_rot, "dof": dof, "fps": fps_out,
            "scale": scale, "source_points": p}


def main() -> int:
    sys.path.insert(0, str(ROOT / "MimicKit" / "mimickit"))
    import anim.mjcf_char_model as mjcf_char_model
    import gait_features as gf

    kin = mjcf_char_model.MJCFCharModel("cpu")
    kin.load(str(ROOT / "MimicKit" / "data" / "assets" / "humanoid" / "humanoid.xml"))
    for path in sys.argv[1:]:
        m = retarget(np.load(path), kin)
        body_pos, body_rot = kin.forward_kinematics(m["root_pos"], m["root_rot"], m["joint_rot"])
        ours = gf.sim_points(body_pos.numpy(), body_rot.numpy(), list(kin.get_body_names()))
        src = m["source_points"]
        src_pts = np.stack([src[:, ms.HML_JOINT[n]] for n in gf.POINTS], axis=1)
        # compare relative to the pelvis (the root path is the same up to the floor offset)
        d = np.linalg.norm((ours - ours[:, :1]) - (src_pts - src_pts[:, :1]), axis=-1)
        print(Path(path).name, "scale %.3f" % m["scale"], "mean point error %.1f cm" % (d.mean() * 100),
              " ".join(f"{n} {d[:, i].mean() * 100:.1f}" for i, n in enumerate(gf.POINTS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
