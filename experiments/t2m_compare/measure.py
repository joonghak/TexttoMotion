#!/home/jong/isaaclab/.venv/bin/python
"""Measurements for the comparison with text-to-motion (T2M) models: the numbers a command states, and physical
plausibility, from the same canonical points for every method.

Usage on this computer:
    ./experiments/t2m_compare/measure.py hml <joints.npy> [...]          # T2M output: HumanML3D joints [T, 22, 3]
    ./experiments/t2m_compare/measure.py ours <rollout.npz> [...]        # our policy, recorded by record_policies.py

Inputs:
- T2M models trained on HumanML3D give 22 SMPL joint positions per frame (metres, y up, 20 fps; the floor is y = 0
  because HumanML3D puts the lowest foot joint of each clip on it). They are turned to z up and mapped to the
  canonical points of experiments/style_eval/gait_features.py.
- Our policies are recorded in Isaac Lab (30 Hz, body positions and rotations); the canonical points come from
  gait_features.sim_points, and the soles from the foot boxes of humanoid.xml.

Numbers (steady straight walking only, as in gait_features.features): torso lean (pelvis-to-neck line), the upper
body's lean above the waist (upper_lean: waist-to-neck line; our trunk joint, HumanML3D spine2), head pitch, cadence, speed,
step length, knee bend, toe-out (from gait_features), and three angles measured here in the walker's heading frame:
arm_flexion (upper arm forward from hanging, deg), arm_abduction (upper arm sideways from hanging, deg) and
leg_abduction (hip-to-ankle line sideways from vertical, deg).

Physics (every frame): the lowest foot point is the lowest of the four foot joints (T2M) or of the foot box corners
(ours). penetration_cm = mean depth of the lowest foot point below the floor; floating_cm = mean height of the lowest
foot point above 1 cm (a walk always has a foot on the floor); slide_cm = how far a planted foot travels over the
floor: for every stance of each foot (the ankle less than 1.5 cm above its lowest level for at least 0.15 s) the
horizontal travel of the ankle over the middle 60% of the stance (heel strike and toe off left out), median over
stances; skate = share of those stance frames in which the ankle moves faster than 0.5 m/s over the floor (2.5 cm
per frame at 20 fps, the threshold of the foot-skating ratio of GMD, Karunratanakul et al. 2023). The ankle is used
because a toe point stays low through the swing of a shuffling walk; a planted foot of a simulated character
cannot move unless it slips.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "style_eval"))

import gait_features as gf  # noqa: E402

HML_FPS = 20.0
# canonical point -> SMPL joint index of HumanML3D (0 pelvis, 1/2 hips, 4/5 knees, 7/8 ankles, 10/11 feet, 12 neck,
# 15 head, 16/17 shoulders, 18/19 elbows, 20/21 wrists; odd indices of a pair are left)
HML_JOINT = {"pelvis": 0, "neck": 12, "head": 15, "r_shoulder": 17, "r_elbow": 19, "r_wrist": 21,
             "l_shoulder": 16, "l_elbow": 18, "l_wrist": 20, "r_hip": 2, "r_knee": 5, "r_ankle": 8, "r_toe": 11,
             "l_hip": 1, "l_knee": 4, "l_ankle": 7, "l_toe": 10}
HML_FOOT = [7, 8, 10, 11]
# The waist: our humanoid bends its trunk at one joint, 0.236 m above the pelvis on a 0.460 m pelvis-neck line (51 %);
# HumanML3D's spine2 sits at 49 % of that line (0.263 of 0.536 m), spine1 at 24 %.
HML_WAIST = 6
FOOT_BOX = (np.array([0.045, 0.0, -0.0225]), np.array([0.0885, 0.045, 0.0275]))  # centre, half size, foot frame
SKATE_V, FLOAT_TOL = 0.5, 0.01


def hml_points(joints: np.ndarray) -> np.ndarray:
    """[T, 22, 3] y-up HumanML3D joints -> [T, 17, 3] z-up canonical points (forward z -> x, left x -> y, up y -> z)."""
    j = np.asarray(joints, dtype=np.float64)[..., [2, 0, 1]]
    return np.stack([j[:, HML_JOINT[name]] for name in gf.POINTS], axis=1)


def hml_lowest(joints: np.ndarray) -> np.ndarray:
    return np.asarray(joints, dtype=np.float64)[:, HML_FOOT, 1].min(axis=1)


def sim_lowest(body_pos: np.ndarray, body_rot: np.ndarray, body_names: list) -> np.ndarray:
    """Height of the lowest foot box corner per frame (our humanoid)."""
    corners = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]) * FOOT_BOX[1] + FOOT_BOX[0]
    low = []
    for foot in ("right_foot", "left_foot"):
        b = body_names.index(foot)
        q = np.repeat(body_rot[:, b:b + 1], 8, axis=1)
        world = body_pos[:, b:b + 1] + gf._quat_apply(q, np.broadcast_to(corners, q.shape[:2] + (3,)))
        low.append(world[..., 2].min(axis=1))
    return np.minimum(*low)


def steady_frames(points: np.ndarray, fps: float):
    """Heading axes and the steady-walking mask of gait_features.features."""
    pelvis = points[:, gf.IDX["pelvis"]]
    path = gf._smooth(pelvis[:, :2], fps)
    vel = np.gradient(path, 1.0 / fps, axis=0)
    speed = np.linalg.norm(vel, axis=-1)
    heading = np.unwrap(np.arctan2(vel[:, 1], vel[:, 0]))
    turn = np.degrees(np.abs(np.gradient(gf._smooth(heading, fps), 1.0 / fps)))
    keep = (speed > 0.5 * np.median(speed)) & (turn < 20.0)
    edge = int(fps)
    keep[:edge] = False
    keep[-edge:] = False
    fwd = np.stack([np.cos(heading), np.sin(heading), np.zeros_like(heading)], axis=-1)
    left = np.stack([-np.sin(heading), np.cos(heading), np.zeros_like(heading)], axis=-1)
    return fwd, left, keep


def extra_angles(points: np.ndarray, fps: float) -> dict:
    fwd, left, k = steady_frames(points, fps)
    g = lambda name: points[:, gf.IDX[name]]  # noqa: E731
    flex, abd, leg = [], [], []
    for s, out in (("r", -1.0), ("l", 1.0)):
        upper = g(s + "_elbow") - g(s + "_shoulder")
        down = -upper[:, 2]
        flex.append(np.degrees(np.arctan2(np.sum(upper * fwd, axis=-1), down))[k].mean())
        abd.append(np.degrees(np.arctan2(out * np.sum(upper * left, axis=-1), down))[k].mean())
        limb = g(s + "_ankle") - g(s + "_hip")
        leg.append(np.degrees(np.arctan2(out * np.sum(limb * left, axis=-1), -limb[:, 2]))[k].mean())
    return {"arm_flexion": float(np.mean(flex)), "arm_abduction": float(np.mean(abd)), "leg_abduction": float(np.mean(leg))}


def stance_intervals(height: np.ndarray, fps: float, margin: float = 0.015, min_s: float = 0.15) -> list:
    rest = np.percentile(height, 2)
    contact = np.append(height < rest + margin, False)
    out, start = [], None
    for t, c in enumerate(contact):
        if c and start is None:
            start = t
        elif not c and start is not None:
            if (t - start) / fps >= min_s:
                out.append((start, t))
            start = None
    return out


def physics(lowest: np.ndarray, ankles: np.ndarray, fps: float) -> dict:
    """lowest [T] heights of the lowest foot point; ankles [T, 2, 3] the two ankle points (z up)."""
    slides, fast, frames = [], 0, 0
    for s in range(2):
        a = ankles[:, s]
        speed = np.append(np.linalg.norm(np.diff(a[:, :2], axis=0), axis=-1) * fps, 0.0)
        for start, end in stance_intervals(a[:, 2], fps):
            lo, hi = start + int(0.2 * (end - start)), start + int(0.8 * (end - start))
            slides.append(float(np.linalg.norm(a[hi, :2] - a[lo, :2])))
            fast += int((speed[lo:hi] > SKATE_V).sum())
            frames += hi - lo
    return {"penetration_cm": float(np.mean(np.maximum(0.0, -lowest)) * 100.0),
            "floating_cm": float(np.mean(np.maximum(0.0, lowest - FLOAT_TOL)) * 100.0),
            "slide_cm": float(np.median(slides) * 100.0) if slides else float("nan"),
            "skate": float(fast / frames) if frames else float("nan"), "stances": len(slides)}


def upper_lean(points: np.ndarray, waist: np.ndarray, fps: float) -> float:
    """Forward lean (deg) of the upper body above the waist: the waist-to-neck line from vertical, steady frames."""
    fwd, _, k = steady_frames(points, fps)
    line = points[:, gf.IDX["neck"]] - waist
    return float(np.degrees(np.arctan2(np.sum(line * fwd, axis=-1), line[:, 2]))[k].mean())


def measure_points(points: np.ndarray, fps: float, lowest: np.ndarray, waist: np.ndarray | None = None) -> dict:
    out = {"frames": int(len(points)), "fps": fps}
    try:
        feats = gf.features(points, fps, min_frames=int(2 * fps))
        out.update({k: feats[k] for k in ("torso_lean", "head_pitch", "cadence", "knee_bend", "toe_out")})
        out["speed"] = feats["_speed"]
        out["step_length_m"] = feats["step_length"] * feats["_leg"]
        out.update(extra_angles(points, fps))
        if waist is not None:
            out["upper_lean"] = upper_lean(points, waist, fps)
        out["steady_frames"] = feats["_frames"]
    except ValueError as exc:
        out["error"] = str(exc)
    ankles = points[:, [gf.IDX["r_ankle"], gf.IDX["l_ankle"]]]
    out.update(physics(lowest, ankles, fps))
    return out


def measure_hml(path: Path) -> dict:
    joints = np.load(path, allow_pickle=False)
    if joints.ndim == 4:  # [1, T, 22, 3]
        joints = joints[0]
    waist = np.asarray(joints, dtype=np.float64)[..., [2, 0, 1]][:, HML_WAIST]
    return measure_points(hml_points(joints), HML_FPS, hml_lowest(joints), waist)


def measure_ours(path: Path) -> list:
    data = np.load(path, allow_pickle=True)
    names = list(data["body_names"])
    fps = 1.0 / float(data["dt"])
    results = []
    for n in range(data["body_pos"].shape[1]):
        resets = np.nonzero(data["reset"][:, n])[0]
        # the longest stretch without a reset (from 5 frames after one): the whole recording when the character never
        # fell, and one whole chain of actions when the chain starts again at every end (the last stretch of the
        # recording is cut off by its end, so it can hold only the first action of the chain)
        cuts = [0, *(int(r) for r in resets), data["body_pos"].shape[0]]
        start, end = max(((a + 5 if a else 0, b) for a, b in zip(cuts[:-1], cuts[1:])), key=lambda s: s[1] - s[0])
        pos, rot = data["body_pos"][start:end, n].astype(np.float64), data["body_rot"][start:end, n].astype(np.float64)
        points = gf.sim_points(pos, rot, names)
        results.append(measure_points(points, fps, sim_lowest(pos, rot, names), pos[:, names.index("torso")]))
    return results


def main() -> int:
    kind, paths = sys.argv[1], [Path(p) for p in sys.argv[2:]]
    for path in paths:
        result = measure_hml(path) if kind == "hml" else measure_ours(path)
        print(json.dumps({"file": path.name, "result": result}, default=float))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
