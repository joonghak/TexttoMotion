"""100STYLE forward walks moved onto our humanoid, for looking at them next to our policies (not for the metric).

The 100STYLE skeleton and MimicKit's humanoid.xml both stand in a T-pose with every joint frame aligned to the world
when all joint angles are zero (BVH: y up, facing +z, left +x; ours: z up, facing +x, left +y). So the global
rotation of each 100STYLE joint, written in our axes (C R C^T), is the global rotation of the matching body of our
character, twist included; the local joint rotations follow from the parent's. Our one-axis elbows and knees keep the
part of the rotation about their axis. The pelvis path is scaled by the ratio of leg lengths (ours 0.83 m, the
actor's 0.87 m) and lowered or raised in every frame so that the lowest corner of the two feet touches the ground.
Chosen stretch: the part of the forward walk that turns least. The actor walks round the capture area, so even that
part turns (120 to 260 degrees in 10 s); the turning is taken out: each frame is turned about the vertical by minus
its direction of travel and the pelvis path is rebuilt from its steps, so the walk goes along +x.

Used by film_compare.py; check: ./retarget_100style.py Zombie (prints the gait features of the retargeted clip).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import gait_features as gf  # noqa: E402

DATA = Path("/home/jong/datasets/100STYLE")
STEP = 2                          # 60 fps -> 30 fps, our control rate
FPS = 60.0 / STEP
# our body -> the 100STYLE joint whose global rotation it takes
BODY_JOINT = {"pelvis": "Hips", "torso": "Chest4", "head": "Head",
              "right_upper_arm": "RightShoulder", "right_lower_arm": "RightElbow", "right_hand": "RightWrist",
              "left_upper_arm": "LeftShoulder", "left_lower_arm": "LeftElbow", "left_hand": "LeftWrist",
              "right_thigh": "RightHip", "right_shin": "RightKnee", "right_foot": "RightAnkle",
              "left_thigh": "LeftHip", "left_shin": "LeftKnee", "left_foot": "LeftAnkle"}
C = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])   # BVH axes -> ours
OUR_LEG = 0.421546 + 0.409870                                       # hip -> knee -> ankle, humanoid.xml
FOOT_BOX = (np.array([0.045, 0.0, -0.0225]), np.array([0.0885, 0.045, 0.0275]))  # centre, half size, foot frame


def frame_cut(style: str):
    rows = {row["STYLE_NAME"]: row for row in csv.DictReader(open(DATA / "raw" / "Frame_Cuts.csv"))}
    return int(rows[style]["FW_START"]), int(rows[style]["FW_STOP"])


def bvh_globals(style: str):
    """Global rotations (scipy Rotation per joint) and positions [T, J, 3] (cm, BVH axes) of the forward walk."""
    from scipy.spatial.transform import Rotation

    names, parents, offsets, channels, motion, _ = gf.read_bvh(DATA / "FW" / f"{style}_FW.bvh")
    start, stop = frame_cut(style)
    motion = motion[start:stop:STEP]
    num = len(motion)
    rot, pos = [None] * len(names), [None] * len(names)
    column = 0
    for j, (parent, chans) in enumerate(zip(parents, channels)):
        values = motion[:, column:column + len(chans)]
        column += len(chans)
        trans = np.zeros((num, 3))
        order, angles = "", []
        for c, name in enumerate(chans):
            if name.endswith("position"):
                trans[:, "XYZ".index(name[0])] = values[:, c]
            else:
                order += name[0]
                angles.append(values[:, c])
        local = Rotation.from_euler(order, np.stack(angles, axis=-1), degrees=True) if order else Rotation.identity(num)
        if parent < 0:
            rot[j], pos[j] = local, trans + offsets[j]
        else:
            rot[j] = rot[parent] * local
            pos[j] = pos[parent] + rot[parent].apply(np.broadcast_to(offsets[j], (num, 3)))
    index = {name: j for j, name in enumerate(names)}
    leg = (np.linalg.norm(offsets[index["RightKnee"]]) + np.linalg.norm(offsets[index["RightAnkle"]])) * 0.01
    return names, rot, np.stack(pos, axis=1), index, leg


def heading_of(path_xy: np.ndarray):
    """Smoothed direction of travel (rad, unwrapped) and speed (m/s) per frame of a path in metres."""
    vel = np.gradient(gf._smooth(path_xy, int(FPS)), axis=0) * FPS
    return np.unwrap(np.arctan2(vel[:, 1], vel[:, 0])), np.linalg.norm(vel, axis=1)


def steadiest(heading: np.ndarray, speed: np.ndarray, frames: int) -> int:
    """Start of the window of `frames` frames with the least mean turning, walking all the time.

    The actor walks round the capture area, so ten seconds always contain turns (120 to 260 degrees); retarget()
    takes the turning out afterwards."""
    turn = np.abs(np.gradient(gf._smooth(heading[:, None], int(FPS))[:, 0]))
    best, best_turn = 0, np.inf
    for s in range(0, len(heading) - frames, 5):
        if speed[s:s + frames].min() < 0.12:
            continue
        mean_turn = turn[s:s + frames].mean()
        if mean_turn < best_turn:
            best, best_turn = s, mean_turn
    return best


def retarget(style: str, seconds: float, kin, device: str = "cpu"):
    """Root positions [T, 3], root rotations [T, 4] (x, y, z, w), joint rotations [T, J-1, 4] and dofs [T, D] of
    `seconds` of the straightest stretch of the style's forward walk, on our character (kin: KinCharModel)."""
    import torch
    from scipy.spatial.transform import Rotation

    names, rot, pos, index, leg = bvh_globals(style)
    ratio = OUR_LEG / leg
    hips = pos[:, index["Hips"]] * 0.01 @ C.T * ratio               # metres, our axes, our size
    heading, speed = heading_of(hips[:, :2])
    frames = int(round(seconds * FPS))
    start = steadiest(heading, speed, frames)
    sl = slice(start, start + frames)
    # Take the turning out: every frame is turned about the vertical by minus its smoothed direction of travel, and
    # the pelvis path is rebuilt from its steps turned the same way. The walk then goes along +x; the pose relative
    # to the direction of travel, the side-to-side sway and the height of the pelvis stay as captured.
    psi = heading[sl]
    steps = np.diff(hips[sl, :2], axis=0)
    cos, sin = np.cos(-psi[:-1]), np.sin(-psi[:-1])
    steps = np.stack([cos * steps[:, 0] - sin * steps[:, 1], sin * steps[:, 0] + cos * steps[:, 1]], axis=1)
    xy = np.concatenate([np.zeros((1, 2)), np.cumsum(steps, axis=0)])
    root_pos = np.column_stack([xy, hips[sl, 2]])
    c_rot = Rotation.from_matrix(C)
    body_names = kin.get_body_names()
    glob = [c_rot * rot[index[BODY_JOINT[b]]][sl] * c_rot.inv() for b in body_names]
    joint_rot = []
    for j in range(1, len(body_names)):
        parent = kin.get_parent_id(j)
        joint_rot.append((glob[parent].inv() * glob[j]).as_quat())
    joint_rot = torch.tensor(np.stack(joint_rot, axis=1), dtype=torch.float32, device=device)
    root_rot = torch.tensor((Rotation.from_euler("z", -psi) * glob[0]).as_quat(), dtype=torch.float32, device=device)
    root_pos = torch.tensor(root_pos, dtype=torch.float32, device=device)
    dof = kin.rot_to_dof(joint_rot)
    joint_rot = kin.dof_to_rot(dof)                                  # one-axis joints keep their axis part
    # ground contact: the lowest foot corner of every frame at z = 0 (one foot is always down in a walk)
    body_pos, body_rot = kin.forward_kinematics(root_pos, root_rot, joint_rot)
    corners = torch.tensor([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)],
                           dtype=torch.float32, device=device) * torch.tensor(FOOT_BOX[1], dtype=torch.float32,
                                                                               device=device)
    corners = corners + torch.tensor(FOOT_BOX[0], dtype=torch.float32, device=device)
    lowest = []
    for foot in ("right_foot", "left_foot"):
        b = body_names.index(foot)
        q = body_rot[:, b:b + 1].expand(-1, 8, -1)
        world = body_pos[:, b:b + 1] + quat_rotate(q, corners.expand(len(q), -1, -1))
        lowest.append(world[..., 2].min(dim=1).values)
    ground = torch.minimum(*lowest)
    root_pos[:, 2] -= torch.tensor(gf._smooth(ground.cpu().numpy(), 3), dtype=torch.float32, device=device)
    return {"root_pos": root_pos, "root_rot": root_rot, "joint_rot": joint_rot, "dof": dof, "fps": FPS,
            "start_frame": start * STEP + frame_cut(style)[0], "ratio": ratio}


def quat_rotate(q, v):
    """Rotate v [..., 3] by quaternions q [..., 4] (x, y, z, w), torch."""
    import torch
    xyz, w = q[..., :3], q[..., 3:]
    t = 2.0 * torch.cross(xyz, v, dim=-1)
    return v + w * t + torch.cross(xyz, t, dim=-1)


def main() -> int:
    """Gait-feature check: the retargeted clip against the original, as a style difference from retargeted Neutral."""
    sys.path.insert(0, str(HERE.parents[1] / "MimicKit" / "mimickit"))
    import anim.mjcf_char_model as mjcf_char_model
    import style_metric as sm

    kin = mjcf_char_model.MJCFCharModel("cpu")
    kin.load(str(HERE.parents[1] / "MimicKit" / "data" / "assets" / "humanoid" / "humanoid.xml"))
    ref = sm.Reference()

    def feats(style):
        m = retarget(style, 20.0, kin)
        body_pos, body_rot = kin.forward_kinematics(m["root_pos"], m["root_rot"], m["joint_rot"])
        points = gf.sim_points(body_pos.numpy(), body_rot.numpy(), list(kin.get_body_names()))
        return gf.features(points, FPS)

    plain = feats("Neutral")
    plain["toe_out"] = ref.raw["plain_features"]["toe_out"] + plain["toe_out"] - ref.raw["styles"]["Neutral"]["features"]["toe_out"]
    for style in sys.argv[1:] or ["Zombie"]:
        delta = gf.style_delta(feats(style), plain)
        print(style, ref.evaluate(delta, style))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
