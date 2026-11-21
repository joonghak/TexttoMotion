"""Gait features of a forward walk, the same for 100STYLE motion capture and for our simulated humanoid.

A walk is given as global positions [T, J, 3] (metres, z up) of the canonical points below at a known frame rate.
Every feature is measured in the walker's heading frame (forward = the smoothed direction of travel), only on
frames of steady straight walking, and is scaled by the walker's own leg or arm length, so that two skeletons of
different size can be compared. A style is then described by how its features differ from the same skeleton's
plain walk (style_delta): the 100STYLE style against 100STYLE Neutral, our policy against our base walk.

Canonical points: pelvis, neck (base of the neck), head (top of the head), and per side shoulder, elbow, wrist,
hip, knee, ankle, toe.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

POINTS = ["pelvis", "neck", "head",
          "r_shoulder", "r_elbow", "r_wrist", "l_shoulder", "l_elbow", "l_wrist",
          "r_hip", "r_knee", "r_ankle", "r_toe", "l_hip", "l_knee", "l_ankle", "l_toe"]
IDX = {name: i for i, name in enumerate(POINTS)}

# name -> (meaning, how a style difference is taken: "log" ratio or plain "diff")
FEATURES = {
    "step_length": ("step length / leg length", "log"),
    "cadence": ("steps per minute", "log"),
    "torso_lean": ("torso forward lean (deg)", "diff"),
    "torso_side": ("torso side tilt range (deg)", "diff"),
    "head_pitch": ("head pitch relative to the torso, forward + (deg)", "diff"),
    "arm_swing": ("wrist fore-aft range / arm length", "diff"),
    "hand_forward": ("wrist ahead of the pelvis / arm length", "diff"),
    "hand_height": ("wrist above the shoulder / arm length (-1 hanging)", "diff"),
    "hand_out": ("wrist outside the shoulder / arm length", "diff"),
    "elbow_bend": ("elbow flexion (deg)", "diff"),
    "knee_bend": ("knee flexion (deg)", "diff"),
    "pelvis_height": ("pelvis above the ground / leg length", "diff"),
    "foot_lift": ("ankle height range / leg length", "diff"),
    "stance_width": ("ankles apart sideways / leg length", "diff"),
    "pelvis_sway": ("pelvis sideways range / leg length", "diff"),
    "head_sway": ("head sideways range / leg length", "diff"),
    "bounce": ("pelvis up-down range / leg length", "diff"),
    "toe_out": ("foot turned outward (deg)", "diff"),
}


def _smooth(x: np.ndarray, frames: int) -> np.ndarray:
    """Centred moving average along axis 0 (edges padded with the end values)."""
    frames = max(1, int(frames) | 1)
    if frames == 1:
        return x
    pad = frames // 2
    padded = np.concatenate([np.repeat(x[:1], pad, axis=0), x, np.repeat(x[-1:], pad, axis=0)], axis=0)
    kernel = np.ones(frames) / frames
    flat = padded.reshape(len(padded), -1)
    out = np.stack([np.convolve(flat[:, k], kernel, mode="valid") for k in range(flat.shape[1])], axis=1)
    return out.reshape((len(x),) + x.shape[1:])


def _range(x: np.ndarray) -> float:
    return float(np.percentile(x, 95) - np.percentile(x, 5))


def _angle(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    cos = np.sum(a * b, axis=-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1) + 1e-9)
    return np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))


def features(points: np.ndarray, fps: float, min_frames: int = 60) -> dict:
    """Gait features of one walk; points [T, len(POINTS), 3], metres, z up."""
    p = points.astype(np.float64)
    pelvis = p[:, IDX["pelvis"]]
    # heading from the smoothed horizontal travel (1 s window), steady straight walking only
    path = _smooth(pelvis[:, :2], fps)
    vel = np.gradient(path, 1.0 / fps, axis=0)
    speed = np.linalg.norm(vel, axis=-1)
    heading = np.unwrap(np.arctan2(vel[:, 1], vel[:, 0]))
    turn = np.degrees(np.abs(np.gradient(_smooth(heading, fps), 1.0 / fps)))
    keep = (speed > 0.5 * np.median(speed)) & (turn < 20.0)
    edge = int(fps)  # drop the first and last second
    keep[:edge] = False
    keep[-edge:] = False
    if keep.sum() < min_frames:
        raise ValueError(f"too few steady walking frames ({keep.sum()})")
    fwd = np.stack([np.cos(heading), np.sin(heading), np.zeros_like(heading)], axis=-1)
    left = np.stack([-np.sin(heading), np.cos(heading), np.zeros_like(heading)], axis=-1)
    up = np.array([0.0, 0.0, 1.0])

    def g(name):
        return p[:, IDX[name]]

    def along(v, axis):
        return np.sum(v * axis, axis=-1)

    leg = np.mean([np.linalg.norm(g(s + "_hip") - g(s + "_knee"), axis=-1).mean()
                   + np.linalg.norm(g(s + "_knee") - g(s + "_ankle"), axis=-1).mean() for s in ("r", "l")])
    arm = np.mean([np.linalg.norm(g(s + "_shoulder") - g(s + "_elbow"), axis=-1).mean()
                   + np.linalg.norm(g(s + "_elbow") - g(s + "_wrist"), axis=-1).mean() for s in ("r", "l")])
    k = keep
    out = {}

    # pace: steps from the sign changes of the ankles' fore-aft difference
    diff = _smooth(along(g("l_ankle") - g("r_ankle"), fwd), max(3, fps // 10))
    sign = np.sign(diff)
    crossings = np.nonzero((sign[1:] != sign[:-1]) & k[1:])[0]
    gaps = np.diff(crossings) / fps
    gaps = gaps[(gaps > 0.15) & (gaps < 2.0)]
    step_time = float(np.median(gaps)) if len(gaps) else float("nan")
    out["cadence"] = 60.0 / step_time
    out["step_length"] = float(np.mean(speed[k])) * step_time / leg

    torso = g("neck") - pelvis
    lean = np.degrees(np.arctan2(along(torso, fwd), torso[:, 2]))
    side = np.degrees(np.arctan2(along(torso, left), torso[:, 2]))
    out["torso_lean"] = float(np.mean(lean[k]))
    out["torso_side"] = _range(side[k])
    head = g("head") - g("neck")
    head_lean = np.degrees(np.arctan2(along(head, fwd), head[:, 2]))
    out["head_pitch"] = float(np.mean((head_lean - lean)[k]))

    swing, ahead, height, outward, elbow = [], [], [], [], []
    for s, sign_out in (("r", -1.0), ("l", 1.0)):
        wrist, shoulder = g(s + "_wrist"), g(s + "_shoulder")
        rel = wrist - pelvis
        swing.append(_range(along(rel, fwd)[k]) / arm)
        ahead.append(float(np.mean(along(rel, fwd)[k])) / arm)
        height.append(float(np.mean((wrist - shoulder)[k, 2])) / arm)
        outward.append(float(np.mean(sign_out * along(wrist - shoulder, left)[k])) / arm)
        elbow.append(float(np.mean(180.0 - _angle(shoulder - g(s + "_elbow"), wrist - g(s + "_elbow"))[k])))
    # one-sided values (2026-11-12), not part of FEATURES: each side alone; signed side angles are + toward the right
    head_side = np.degrees(np.arctan2(along(head, left), head[:, 2]))
    one_side = {"torso_roll": -float(np.mean(side[k])), "head_roll": -float(np.mean((head_side - side)[k]))}
    for i, s in enumerate(("r", "l")):
        one_side.update({f"{s}_arm_swing": swing[i], f"{s}_hand_forward": ahead[i], f"{s}_hand_height": height[i],
                         f"{s}_hand_out": outward[i], f"{s}_elbow_bend": elbow[i]})
    out["arm_swing"], out["hand_forward"] = float(np.mean(swing)), float(np.mean(ahead))
    out["hand_height"], out["hand_out"], out["elbow_bend"] = float(np.mean(height)), float(np.mean(outward)), float(np.mean(elbow))

    knee, lift, toe = [], [], []
    ground = float(np.percentile(np.minimum(g("r_ankle")[:, 2], g("l_ankle")[:, 2])[k], 1))
    for s, sign_out in (("r", -1.0), ("l", 1.0)):
        knee.append(float(np.mean(180.0 - _angle(g(s + "_hip") - g(s + "_knee"), g(s + "_ankle") - g(s + "_knee"))[k])))
        lift.append(_range(g(s + "_ankle")[k, 2]) / leg)
        foot = g(s + "_toe") - g(s + "_ankle")
        toe.append(float(np.mean(np.degrees(np.arctan2(sign_out * along(foot, left), along(foot, fwd)))[k])))
        flexion = 180.0 - _angle(g(s + "_hip") - g(s + "_knee"), g(s + "_ankle") - g(s + "_knee"))
        low = k & (g(s + "_toe")[:, 2] <= np.percentile(g(s + "_toe")[k, 2], 30))  # that foot on the ground
        one_side.update({f"{s}_knee_bend": knee[-1], f"{s}_knee_range": _range(flexion[k]), f"{s}_foot_lift": lift[-1],
                         f"{s}_toe_out": toe[-1],
                         f"{s}_heel_raise": float(np.mean(g(s + "_ankle")[low, 2] - g(s + "_toe")[low, 2])) / leg})
    out["knee_bend"], out["foot_lift"], out["toe_out"] = float(np.mean(knee)), float(np.mean(lift)), float(np.mean(toe))
    out["_side"] = {name: round(value, 4) for name, value in one_side.items()}
    out["pelvis_height"] = float(np.mean(pelvis[k, 2] - ground)) / leg
    out["stance_width"] = float(np.mean(np.abs(along(g("l_ankle") - g("r_ankle"), left))[k])) / leg

    def sway(point):
        rel = np.concatenate([point[:, :2] - path, np.zeros((len(point), 1))], axis=-1)
        return _range(along(rel, left)[k]) / leg

    out["pelvis_sway"], out["head_sway"] = sway(pelvis), sway(g("head"))
    out["bounce"] = _range((pelvis[:, 2] - _smooth(pelvis[:, 2], fps))[k]) / leg
    out["_frames"] = int(k.sum())
    out["_speed"] = float(np.mean(speed[k]))
    out["_leg"], out["_arm"] = float(leg), float(arm)
    return out


def style_delta(style: dict, plain: dict) -> np.ndarray:
    """How a walk differs from the same skeleton's plain walk, one value per FEATURES entry."""
    values = []
    for name, (_, kind) in FEATURES.items():
        a, b = style[name], plain[name]
        values.append(math.log(a / b) if kind == "log" else a - b)
    return np.asarray(values)


# ---- 100STYLE BVH ----

BVH_POINTS = {"pelvis": "Hips", "neck": "Neck", "head": "Head_end",
              "r_shoulder": "RightShoulder", "r_elbow": "RightElbow", "r_wrist": "RightWrist",
              "l_shoulder": "LeftShoulder", "l_elbow": "LeftElbow", "l_wrist": "LeftWrist",
              "r_hip": "RightHip", "r_knee": "RightKnee", "r_ankle": "RightAnkle", "r_toe": "RightToe",
              "l_hip": "LeftHip", "l_knee": "LeftKnee", "l_ankle": "LeftAnkle", "l_toe": "LeftToe"}


def read_bvh(path: Path):
    """(joint names, parents, offsets [J, 3], channels per joint, motion [F, C], frame time); end sites as <parent>_end."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        lines = handle.read().splitlines()
    names, parents, offsets, channels = [], [], [], []
    stack, current, i = [], -1, 0
    while i < len(lines):
        tokens = lines[i].split()
        i += 1
        if not tokens:
            continue
        if tokens[0] in ("ROOT", "JOINT", "End"):
            name = tokens[1] if tokens[0] != "End" else names[stack[-1]] + "_end"
            names.append(name)
            parents.append(stack[-1] if stack else -1)
            offsets.append(np.zeros(3))
            channels.append([])
            current = len(names) - 1
        elif tokens[0] == "{":
            stack.append(current)
        elif tokens[0] == "}":
            stack.pop()
        elif tokens[0] == "OFFSET":
            offsets[current] = np.array([float(v) for v in tokens[1:4]])
        elif tokens[0] == "CHANNELS":
            channels[current] = tokens[2:2 + int(tokens[1])]
        elif tokens[0] == "MOTION":
            break
    num_frames = int(lines[i].split()[1])
    frame_time = float(lines[i + 1].split()[2])
    motion = np.array([[float(v) for v in line.split()] for line in lines[i + 2:i + 2 + num_frames]])
    return names, parents, np.stack(offsets), channels, motion, frame_time


def bvh_points(path: Path, start: int = 0, stop: int | None = None, step: int = 2):
    """Canonical points [T, J, 3] in metres, z up, and the frame rate (every step-th frame)."""
    from scipy.spatial.transform import Rotation

    names, parents, offsets, channels, motion, frame_time = read_bvh(path)
    motion = motion[start:stop:step]
    num = len(motion)
    rot = [None] * len(names)
    pos = [None] * len(names)
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
    points = np.stack([pos[index[BVH_POINTS[name]]] for name in POINTS], axis=1) * 0.01  # cm -> m
    points = points[..., [0, 2, 1]] * np.array([1.0, -1.0, 1.0])  # y up -> z up, right-handed
    return points, 1.0 / (frame_time * step)


# ---- our humanoid (MimicKit humanoid.xml) ----

SIM_BODIES = ["pelvis", "torso", "head", "right_upper_arm", "right_lower_arm", "right_hand",
              "left_upper_arm", "left_lower_arm", "left_hand", "right_thigh", "right_shin", "right_foot",
              "left_thigh", "left_shin", "left_foot"]
HEAD_TOP = np.array([0.0, 0.0, 0.27])      # head sphere centre 0.175 + radius 0.095, head frame
TOE = np.array([0.1335, 0.0, -0.0225])     # front of the foot box, foot frame


def _quat_apply(q: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Rotate v by quaternions q [..., 4] in (x, y, z, w) order."""
    xyz, w = q[..., :3], q[..., 3:]
    t = 2.0 * np.cross(xyz, v)
    return v + w * t + np.cross(xyz, t)


def sim_points(body_pos: np.ndarray, body_rot: np.ndarray, body_names: list) -> np.ndarray:
    """Canonical points [T, J, 3] from body positions [T, B, 3] and rotations [T, B, 4] (x, y, z, w)."""
    b = {name: body_names.index(name) for name in SIM_BODIES}

    def at(name):
        return body_pos[:, b[name]]

    def point(name, local):
        return at(name) + _quat_apply(body_rot[:, b[name]], np.broadcast_to(local, body_pos[:, 0].shape))

    table = {"pelvis": at("pelvis"), "neck": at("head"), "head": point("head", HEAD_TOP),
             "r_shoulder": at("right_upper_arm"), "r_elbow": at("right_lower_arm"), "r_wrist": at("right_hand"),
             "l_shoulder": at("left_upper_arm"), "l_elbow": at("left_lower_arm"), "l_wrist": at("left_hand"),
             "r_hip": at("right_thigh"), "r_knee": at("right_shin"), "r_ankle": at("right_foot"),
             "r_toe": point("right_foot", TOE),
             "l_hip": at("left_thigh"), "l_knee": at("left_shin"), "l_ankle": at("left_foot"),
             "l_toe": point("left_foot", TOE)}
    return np.stack([table[name] for name in POINTS], axis=1)
