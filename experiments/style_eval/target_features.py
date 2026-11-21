#!/home/jong/isaaclab/.venv/bin/python
"""Gait features of the style TARGET motions (no training): what the reward asks for, for many parameter sets at once.

Usage on this computer:
    ./experiments/style_eval/target_features.py <sets.json> [--seconds 20]

sets.json: [{"key": ..., "scales": {...}}] in the scales format of variants.json (style_parser.to_scales gives it for
LLM parameters); a set with empty scales is the plain walk. The walk clip and the formula fixed on 2026-11-03 are
used. For every set the env's own target (env._calc_track_targets: the clip with the speed, cadence, swing, pose and
crouch of the set, the pelvis lowered for bent legs) is played kinematically and turned into the canonical points of
gait_features.py. Writes <sets>_targets.json with the features per key. A trained policy follows these targets only
partly (78 to 104 percent for the leans), so this ranks parameter choices; training confirms them.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import train_from_text as tft  # noqa: E402

DEVICE = "cuda:0"
# A walk policy trained with the fixed formula: its config gives the walk clip, the style term and the units.
CONFIG_RUN = ROOT / "experiments" / "style_walk" / "20261101_225050_general_formula" / "n_walk_zombie" / "config"


def targets_inside(sets_file: Path, seconds: float) -> int:
    sys.path.insert(0, str(tft.MIMICKIT / "mimickit"))
    import envs.env_builder as env_builder
    import envs.text_reward_env as text_reward_env
    import util.mp_util as mp_util
    import util.torch_util as torch_util
    import numpy as np
    import torch
    import gait_features as gf

    sets = json.loads(sets_file.read_text())
    num = len(sets)
    env_config, engine_config = env_builder.load_configs(str(CONFIG_RUN / "env_play.yaml"), str(CONFIG_RUN / "engine.yaml"))
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=num,
                                        device=DEVICE, visualize=False)
    kin = env._kin_char_model
    names = kin.get_body_names()
    arm_ids = env._arm_joint_ids
    for i, entry in enumerate(sets):
        scales = entry.get("scales") or {}
        env._speed_scale[i] = float(scales.get("speed", 1.0))
        env._cadence_scale[i] = float(scales.get("cadence", 1.0))
        env._swing_scale[i] = 1.0
        env._swing_scale[i, arm_ids] = float(scales.get("arm_swing", 1.0))
        env._pose_offset[i] = torch.tensor([0.0, 0.0, 0.0, 1.0], device=DEVICE)
        for body, value in (scales.get("swing") or {}).items():
            env._swing_scale[i, names.index(body) - 1] = float(value)
        for body, angles in (scales.get("pose") or {}).items():
            exp_map = torch.tensor([angles], device=DEVICE, dtype=torch.float) * (math.pi / 180.0)
            env._pose_offset[i, names.index(body) - 1] = torch_util.exp_map_to_quat(exp_map)[0]
        env._crouch_angle[i] = math.radians(float(scales.get("crouch", 0.0)))
        env._bounce_angle[i] = math.radians(float(scales.get("bounce", 0.0)))
        env._foot_pitch[i] = math.radians(float(scales.get("foot_pitch", 0.0)))
        env._weave_amp[i] = float(scales.get("weave", 0.0))
    dt = 1.0 / 30.0
    with torch.no_grad():
        env._rand_reset = False
        env.reset()
        env._motion_time_offsets[:] = 0.0
        positions, rotations = [], []
        for step in range(int(seconds / dt)):
            env._time_buf[:] = step * dt
            env._update_ref_motion()
            root_pos, joint_rot, _, _, _ = env._calc_track_targets()
            body_pos, body_rot = kin.forward_kinematics(root_pos, env._ref_root_rot, joint_rot)
            positions.append(body_pos.cpu().numpy())
            rotations.append(body_rot.cpu().numpy())
    positions, rotations = np.stack(positions), np.stack(rotations)
    out = {}
    for i, entry in enumerate(sets):
        try:
            out[entry["key"]] = gf.features(gf.sim_points(positions[:, i], rotations[:, i], names), 1.0 / dt)
        except ValueError as exc:
            out[entry["key"]] = {"error": str(exc)}
    target_file = sets_file.with_name(sets_file.stem + "_targets.json")
    target_file.write_text(json.dumps(out, indent=1))
    print(f"{num} sets -> {target_file}", flush=True)
    return 0


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("sets", type=Path)
    cli.add_argument("--seconds", type=float, default=20.0)
    cli.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    args = cli.parse_args()
    sets = args.sets.resolve()
    if args.inside:
        return targets_inside(sets, args.seconds)
    return tft.run_in_isaaclab([sets, "--seconds", args.seconds, "--inside"],
                               log_file=sets.with_name(sets.stem + "_targets.log"), script=Path(__file__).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
