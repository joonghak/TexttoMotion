"""Measure what a trained run's character actually does (runs inside Isaac Lab, headless).

Started by run_experiment.py through train_from_text.run_in_isaaclab, which activates
Isaac Lab and works from the MimicKit directory:
    rollout_eval.py <run_dir>          -> writes <run_dir>/eval.json

One deterministic rollout (policy mean action) from the start of the reference clip,
until the clip ends or the character falls. The same numbers are computed for the
simulated character ("sim") and for the reference motion over the same time window
("reference_window"). Angles are relative to the unmodified clip, so a reference
rotated by direction 0.25 has start_heading_deg and travel_deg of 90.
"""

from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
from pathlib import Path

import numpy as np

MIMICKIT = Path(__file__).resolve().parents[2] / "MimicKit"
sys.path.insert(0, str(MIMICKIT / "mimickit"))

# Same import order as mimickit/run.py; building the env starts Isaac Lab.
import envs.env_builder as env_builder  # noqa: E402
import learning.agent_builder as agent_builder  # noqa: E402
import envs.base_env as base_env  # noqa: E402
import learning.base_agent as base_agent  # noqa: E402
import util.mp_util as mp_util  # noqa: E402
import util.torch_util as torch_util  # noqa: E402
import torch  # noqa: E402

FOOT_BODIES = ["right_foot", "left_foot"]
KICK_HEIGHT = 0.8  # m; one kick = a foot rising above this (rearmed below half of it)


def wrap360(angle: float) -> float:
    angle %= 360.0
    return 0.0 if angle > 359.5 else angle  # -0.0001 deg is 0, not 360


def clip_angles(clip_file: str) -> tuple:
    """Frame-0 heading and net travel direction (deg) of the unmodified clip."""
    with open(clip_file, "rb") as f:
        frames = torch.tensor(np.nan_to_num(np.asarray(pickle.load(f)["frames"], dtype=np.float32)))
    heading = math.degrees(float(torch_util.calc_heading(torch_util.exp_map_to_quat(frames[0:1, 3:6]))[0]))
    disp = frames[-1, 0:2] - frames[0, 0:2]
    return heading, math.degrees(math.atan2(float(disp[1]), float(disp[0])))


def motion_features(root_pos, heading, foot_z, dt, clip_heading, clip_travel, hand_pos=None, head_pos=None) -> dict:
    """root_pos [T,3], heading [T] (rad), foot_z [T,2], hand_pos [T,2,3], head_pos [T,3]."""
    duration = (len(root_pos) - 1) * dt
    disp = root_pos[-1, 0:2] - root_pos[0, 0:2]
    distance = float(np.linalg.norm(disp))
    turn = np.unwrap(heading)
    total_turn = math.degrees(turn[-1] - turn[0])
    kicks, armed = 0, True
    for z in foot_z.max(axis=1):
        if armed and z > KICK_HEIGHT:
            kicks, armed = kicks + 1, False
        elif z < 0.5 * KICK_HEIGHT:
            armed = True
    style = {}
    if hand_pos is not None:
        # Hand offset from the pelvis along the body's forward direction; swing = its range.
        forward = np.stack([np.cos(heading), np.sin(heading)], axis=-1)
        offset = np.einsum("thc,tc->th", hand_pos[..., 0:2] - root_pos[:, None, 0:2], forward)
        up = head_pos - root_pos
        tilt = np.degrees(np.arctan2(np.linalg.norm(up[:, 0:2], axis=-1), up[:, 2]))
        style = {
            "arm_swing_m": float(np.mean(offset.max(axis=0) - offset.min(axis=0))),
            "foot_clearance_m": float(np.max(foot_z.max(axis=0) - foot_z.min(axis=0))),
            "torso_tilt_deg": float(tilt.mean()),
        }
    return {
        **style,
        "duration_s": duration,
        "start_heading_deg": wrap360(math.degrees(heading[0]) - clip_heading),
        "travel_deg": wrap360(math.degrees(math.atan2(disp[1], disp[0])) - clip_travel),
        "distance_m": distance,
        "speed_mps": distance / duration if duration > 0 else 0.0,
        "total_turn_deg": total_turn,
        "turn_rate_dps": abs(total_turn) / duration if duration > 0 else 0.0,
        "max_foot_height_m": float(foot_z.max()),
        "kick_count": kicks,
    }


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("run_dir")
    cli.add_argument("--device", default="cuda:0")
    args = cli.parse_args()

    run_dir = Path(args.run_dir).resolve()
    config = run_dir / "config"
    summary = json.loads((run_dir / "summary.json").read_text())
    ref_duration = summary["reference"]["duration_s"]

    mp_util.init(0, 1, args.device, int(np.random.randint(6000, 7000)))
    env = env_builder.build_env(str(config / "env_play.yaml"), str(config / "engine.yaml"),
                                1, args.device, visualize=False)
    agent = agent_builder.build_agent(str(config / "agent.yaml"), env, args.device)
    agent.load(str(run_dir / "train" / "model.pt"))
    agent.eval()
    agent.set_mode(base_agent.AgentMode.TEST)

    engine, char_id = env._engine, env._get_char_id()
    foot_ids = env._build_body_ids_tensor(FOOT_BODIES).tolist()
    hand_ids = env._build_body_ids_tensor(["right_hand", "left_hand"]).tolist()
    head_id = int(env._build_body_ids_tensor(["head"])[0])
    dt = float(engine.get_timestep())
    log = {key: [] for key in ("sim_pos", "sim_rot", "sim_body", "ref_pos", "ref_rot", "ref_body")}

    def record():
        log["sim_pos"].append(engine.get_root_pos(char_id)[0].cpu().clone())
        log["sim_rot"].append(engine.get_root_rot(char_id)[0].cpu().clone())
        log["sim_body"].append(engine.get_body_pos(char_id)[0].cpu().clone())
        log["ref_pos"].append(env._ref_root_pos[0].cpu().clone())
        log["ref_rot"].append(env._ref_root_rot[0].cpu().clone())
        log["ref_body"].append(env._ref_body_pos[0].cpu().clone())

    done_flag = base_env.DoneFlags.NULL.value
    with torch.no_grad():
        obs, info = agent._reset_envs()
        record()
        for _ in range(int(math.ceil(ref_duration / dt)) + 30):
            action, _ = agent._decide_action(obs, info)
            obs, _, done, info = agent._step_env(action)
            record()
            done_flag = int(done[0])
            if done_flag != base_env.DoneFlags.NULL.value:
                break

    data = {key: torch.stack(values) for key, values in log.items()}
    clip_heading, clip_travel = clip_angles(summary["reference"]["clip"])
    measured = {}
    for who in ("sim", "ref"):
        heading = torch_util.calc_heading(data[f"{who}_rot"]).numpy()
        body = data[f"{who}_body"].numpy()
        measured[who] = motion_features(data[f"{who}_pos"].numpy(), heading, body[:, foot_ids, 2], dt,
                                        clip_heading, clip_travel, body[:, hand_ids], body[:, head_id])

    root_err = torch.linalg.vector_norm(data["sim_pos"] - data["ref_pos"], dim=-1)
    body_err = torch.linalg.vector_norm(data["sim_body"] - data["ref_body"], dim=-1)
    fell = done_flag == base_env.DoneFlags.FAIL.value
    result = {
        "end": base_env.DoneFlags(done_flag).name,
        "fell": fell,
        "fell_at_s": measured["sim"]["duration_s"] if fell else None,
        "completion": min(1.0, measured["sim"]["duration_s"] / ref_duration),
        "reference_duration_s": ref_duration,
        "sim": measured["sim"],
        "reference_window": measured["ref"],
        "root_pos_err_m": float(root_err.mean()),
        "body_pos_err_m": float(body_err.mean()),
        "dt": dt,
        "steps": len(log["sim_pos"]) - 1,
    }
    (run_dir / "eval.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    sim = measured["sim"]
    print(f"측정 완료: 완주 {result['completion']:.0%}, 이동 {sim['travel_deg']:.0f}°, "
          f"속도 {sim['speed_mps']:.2f} m/s, 회전 {sim['total_turn_deg']:.0f}°, "
          f"발 높이 {sim['max_foot_height_m']:.2f} m, 킥 {sim['kick_count']}회", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
