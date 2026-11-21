"""Canonical gait points of our humanoid from a MimicKit motion clip (kinematic, no simulation)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MIMICKIT = HERE.parents[1] / "MimicKit"
sys.path.insert(0, str(MIMICKIT / "mimickit"))
sys.path.insert(0, str(HERE))

import gait_features as gf  # noqa: E402

CHAR_FILE = MIMICKIT / "data" / "assets" / "humanoid" / "humanoid.xml"
FPS = 30.0


def clip_points(motion_file: Path, seconds: float = 30.0):
    """Points [T, J, 3] of the clip played (looped) for the given time, and the frame rate."""
    import torch
    import anim.mjcf_char_model as mjcf_char_model
    import anim.motion_lib as motion_lib

    kin = mjcf_char_model.MJCFCharModel("cpu")
    kin.load(str(CHAR_FILE))
    lib = motion_lib.MotionLib(str(motion_file), kin, "cpu")
    times = torch.arange(int(seconds * FPS), dtype=torch.float32) / FPS
    ids = torch.zeros_like(times, dtype=torch.long)
    root_pos, root_rot, _, _, joint_rot, _ = lib.calc_motion_frame(ids, times)
    body_pos, body_rot = kin.forward_kinematics(root_pos, root_rot, joint_rot)
    return gf.sim_points(body_pos.numpy(), body_rot.numpy(), kin.get_body_names()), FPS
