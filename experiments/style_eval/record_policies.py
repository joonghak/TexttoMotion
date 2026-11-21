#!/home/jong/isaaclab/.venv/bin/python
"""Record what trained policies do: body positions and rotations of a few characters per policy (30 Hz).

Usage on this computer:
    ./experiments/style_eval/record_policies.py experiments/style_walk/<실험>/<변형> [...] [--seconds 30] [--replicas 4]

All given policies must imitate the same reference clip; they run together in one headless simulation, each
character with its own policy and its own speed and cadence scales (the only style settings the policy observes).
Characters start at the clip start, and an episode lasts longer than the recording, so a reset only follows a fall.
Writes experiments/style_eval/rollouts/<실험>__<변형>.npz: body_pos [T, N, B, 3], body_rot [T, N, B, 4] (x, y, z, w),
reset [T, N] (True on the step a character was reset), body_names, dt.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "style_walk"))

import train_from_text as tft  # noqa: E402
from run_style_walk import read_scales  # noqa: E402

DEVICE = "cuda:0"
OUT = HERE / "rollouts"


def label(run: Path) -> str:
    return f"{run.parent.name}__{run.name}"


def record_inside(runs, seconds: float, replicas: int) -> int:
    """Runs under Isaac Lab from the MimicKit directory."""
    sys.path.insert(0, str(tft.MIMICKIT / "mimickit"))
    import envs.env_builder as env_builder
    import learning.agent_builder as agent_builder
    import envs.base_env as base_env
    import envs.text_reward_env as text_reward_env
    import learning.base_agent as base_agent
    import util.mp_util as mp_util
    import numpy as np
    import torch

    num_runs = len(runs)
    num_envs = num_runs * replicas
    env_config, engine_config = env_builder.load_configs(str(runs[0] / "config" / "env_play.yaml"),
                                                         str(runs[0] / "config" / "engine.yaml"))
    env_config["episode_length"] = seconds + 10.0
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=num_envs,
                                        device=DEVICE, visualize=False)
    engine, char_id = env._engine, env._get_char_id()
    agents = []
    for run in runs:
        agent = agent_builder.build_agent(str(run / "config" / "agent.yaml"), env, DEVICE)
        agent.load(str(run / "train" / "model.pt"))
        agent.eval()
        agent.set_mode(base_agent.AgentMode.TEST)
        agents.append(agent)
    run_of = torch.arange(num_envs, device=DEVICE) % num_runs
    ids_of = [(run_of == r).nonzero(as_tuple=False).flatten() for r in range(num_runs)]
    scales = [read_scales(run) for run in runs]
    env._speed_scale[:] = torch.tensor([s["speed"] for s in scales], device=DEVICE)[run_of]
    env._cadence_scale[:] = torch.tensor([s["cadence"] for s in scales], device=DEVICE)[run_of]
    env._weave_amp[:] = torch.tensor([s.get("weave", 0.0) for s in scales], device=DEVICE)[run_of]

    def act(obs, info):
        actions = None
        for agent, ids in zip(agents, ids_of):
            action = agent._decide_action(obs[ids], info)[0]
            if actions is None:
                actions = torch.zeros([num_envs, action.shape[-1]], device=DEVICE, dtype=action.dtype)
            actions[ids] = action
        return actions

    dt = float(engine.get_timestep())
    null_flag = base_env.DoneFlags.NULL.value
    positions, rotations, resets = [], [], []
    with torch.no_grad():
        env._rand_reset = False
        obs, info = env.reset()
        for _ in range(int(round(seconds / dt))):
            obs, _, done, info = env.step(act(obs, info))
            positions.append(engine.get_body_pos(char_id).cpu().numpy())
            rotations.append(engine.get_body_rot(char_id).cpu().numpy())
            reset = done != null_flag
            resets.append(reset.cpu().numpy())
            reset_ids = reset.nonzero(as_tuple=False).flatten()
            if len(reset_ids) > 0:
                obs, info = env.reset(reset_ids)
    positions, rotations, resets = np.stack(positions), np.stack(rotations), np.stack(resets)
    OUT.mkdir(exist_ok=True)
    names = np.array(env._kin_char_model.get_body_names())
    for r, run in enumerate(runs):
        ids = ids_of[r].cpu().numpy()
        np.savez_compressed(OUT / f"{label(run)}.npz", body_pos=positions[:, ids].astype(np.float32),
                            body_rot=rotations[:, ids].astype(np.float32), reset=resets[:, ids], body_names=names, dt=dt)
        print(f"{label(run)}: {int(resets[:, ids].sum())} resets", flush=True)
    return 0


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("runs", nargs="+", help="학습한 정책 폴더 (config/와 train/model.pt가 있는 변형 폴더)")
    cli.add_argument("--seconds", type=float, default=30.0)
    cli.add_argument("--replicas", type=int, default=4, help="정책마다 캐릭터 수")
    cli.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    args = cli.parse_args()
    runs = [Path(run).absolute() for run in args.runs]  # keep symlinked variant names
    missing = [str(run) for run in runs if not (run / "train" / "model.pt").exists()]
    if missing:
        cli.error("학습된 모델이 없습니다: " + ", ".join(missing))
    if args.inside:
        return record_inside(runs, args.seconds, args.replicas)
    OUT.mkdir(exist_ok=True)
    # One simulation loads one reference clip for every character, so runs on different clips (a chain of actions next
    # to walks) are recorded in separate simulations (2026-11-16: before this, all were played on the first run's clip).
    from run_style_walk import run_clip

    groups = {}
    for run in runs:
        groups.setdefault(run_clip(run), []).append(run)
    code = 0
    for clip, group in groups.items():
        code |= tft.run_in_isaaclab([*group, "--seconds", args.seconds, "--replicas", args.replicas, "--inside"],
                                    log_file=OUT / "record_console.log", script=Path(__file__).resolve())
    return code


if __name__ == "__main__":
    raise SystemExit(main())
