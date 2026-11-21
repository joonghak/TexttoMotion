#!/home/jong/isaaclab/.venv/bin/python
"""Four episodes of one variant in one picture: a 2x2 video per variant (headless).

Usage on this computer:
    ./experiments/style_walk/film_grid.py                                # most recent experiment, every variant
    ./experiments/style_walk/film_grid.py experiments/style_walk/<폴더>
    ./experiments/style_walk/film_grid.py <폴더> --variants s1,s2

Each quadrant follows one character from the side for 10 s; nothing is drawn on the picture.
Top left: the episode from the clip start, as in film.py's walk.mp4. Top right, bottom left,
bottom right: the random-start episodes 1, 2, 3 of film.py --episode N, started at the instants
recorded in film/walk_ep<N>.json. Results go to <폴더>/film/: grid_<variant>.mp4 and .gif
(1920x1080). Every variant is filmed in an Isaac Lab process of its own.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import play_motion  # noqa: E402
import train_from_text as tft  # noqa: E402
from play_compare import COLORS, build_camera, latest_experiment, recolor, write_video  # noqa: E402
from run_style_walk import load_variants  # noqa: E402

DEVICE = "cuda:0"
EPISODES = (1, 2, 3)    # random-start episodes shown next to the one from the clip start
TILE_SIZE = (960, 540)
TILE_HFOV = 60.0        # deg
TILE_DIST = 4.6         # m; the character fills a bit more than half of the height
TILE_PITCH = 6.0        # deg the cameras look down
TILE_SMOOTH = 0.3       # share of the way a camera moves to its character per step
TILE_JUMP = 1.5         # m; further than this (a restart) the camera jumps instead of gliding
LINE_WIDTH = 4          # px between the quadrants
SPREAD = 60.0           # m between the characters (diagonal, so no one else is in the picture)
VIDEO_SECONDS = 10.0


def start_times(exp_dir: Path, key: str) -> list:
    """Where in the clip (s) the four episodes of a variant start."""
    files = [exp_dir / "film" / f"walk_ep{episode}.json" for episode in EPISODES]
    missing = [file.name for file in files if not file.exists()]
    if missing:
        raise SystemExit(f"먼저 film.py --episode N 으로 에피소드를 찍으세요: {', '.join(missing)} 없음")
    return [0.0] + [json.loads(file.read_text())["start_time_s"][key] for file in files]


def launch(exp_dir: Path, variants) -> int:
    missing = [key for key in variants if not (exp_dir / key / "train" / "model.pt").exists()]
    if missing:
        print(f"학습된 모델이 없습니다: {', '.join(missing)} ({exp_dir})", file=sys.stderr)
        return 1
    for key in variants:
        start_times(exp_dir, key)
    os.environ.setdefault("DISPLAY", play_motion.DEFAULT_DISPLAY)
    os.environ.setdefault("XAUTHORITY", play_motion.DEFAULT_XAUTHORITY)
    for key in variants:
        log_file = exp_dir / "film" / f"grid_{key}.log"
        code = tft.run_in_isaaclab([exp_dir, "--inside", "--variants", key], log_file=log_file,
                                   script=Path(__file__).resolve())
        if not (exp_dir / "film" / f"grid_{key}.mp4").exists():
            print(f"촬영 실패: {key} (exit {code}, {log_file})", file=sys.stderr)
            return 1
    return 0


def film_inside(exp_dir: Path, key: str) -> int:
    """Runs under Isaac Lab from the MimicKit directory."""
    sys.path.insert(0, str(tft.MIMICKIT / "mimickit"))
    import envs.env_builder as env_builder
    import learning.agent_builder as agent_builder
    import envs.base_env as base_env
    import envs.text_reward_env as text_reward_env
    import engines.isaac_lab_engine as isaac_lab_engine
    import learning.base_agent as base_agent
    import util.mp_util as mp_util
    import carb
    import numpy as np
    import torch

    run = exp_dir / key
    starts = start_times(exp_dir, key)
    num_envs = len(starts)
    all_keys = [variant for variant, _, _ in load_variants(exp_dir)]

    def layout(self, n):
        slot = torch.arange(n, device=self._device, dtype=torch.float)
        return torch.stack([slot * SPREAD, slot * SPREAD], dim=-1)

    isaac_lab_engine.IsaacLabEngine._compute_env_offsets = layout

    config_dir = run / "config"
    env_config, engine_config = env_builder.load_configs(str(config_dir / "env_play.yaml"), str(config_dir / "engine.yaml"))
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=num_envs,
                                        device=DEVICE, visualize=False, record_video=True)
    engine, char_id = env._engine, env._get_char_id()
    recolor(engine, char_id, [COLORS[all_keys.index(key) % len(COLORS)]] * num_envs)
    agent = agent_builder.build_agent(str(config_dir / "agent.yaml"), env, DEVICE)
    agent.load(str(run / "train" / "model.pt"))
    agent.eval()
    agent.set_mode(base_agent.AgentMode.TEST)
    engine.stop_video_recording()  # test mode starts recording every step; frames are grabbed manually here
    carb.settings.get_settings().set("/rtx/post/aa/op", 4)  # DLAA, as in film.py

    # Every character starts its episode, and starts again after a failure, at its own fixed instant of the clip.
    start = torch.tensor(starts, device=DEVICE, dtype=torch.float)
    resetting = {}
    reset_ref_motion = env._reset_ref_motion

    def reset_at_start(env_ids):
        resetting["ids"] = env_ids
        reset_ref_motion(env_ids)

    env._reset_ref_motion = reset_at_start
    env._sample_motion_times = lambda n: (torch.zeros(n, dtype=torch.long, device=DEVICE), start[resetting["ids"]])

    cameras = [build_camera(engine, f"grid_camera_{i}", TILE_SIZE, TILE_HFOV) for i in range(num_envs)]
    offsets = engine._env_offsets.cpu().numpy()
    pitch = math.radians(TILE_PITCH)
    back = TILE_DIST * np.array([0.0, -math.cos(pitch), math.sin(pitch)])
    centre = None  # [N, 2] ground points the cameras look at

    def shoot():
        """The four characters, each from the side, as one 2x2 picture; None while the renderer warms up."""
        nonlocal centre
        xy = engine.get_root_pos(char_id)[:, 0:2].cpu().numpy() + offsets
        if centre is None:
            centre = xy.copy()
        jumped = np.linalg.norm(xy - centre, axis=-1) > TILE_JUMP
        centre = np.where(jumped[:, None], xy, centre + TILE_SMOOTH * (xy - centre))
        for (look, _), point in zip(cameras, centre):
            target = np.array([point[0], point[1], 0.9])
            look(target + back, target)
        engine.get_sim().render()
        tiles = [read() for _, read in cameras]
        if any(tile is None for tile in tiles):
            return None
        frame = np.vstack([np.hstack(tiles[0:2]), np.hstack(tiles[2:4])])
        half = LINE_WIDTH // 2
        frame[TILE_SIZE[1] - half:TILE_SIZE[1] + half, :] = 60
        frame[:, TILE_SIZE[0] - half:TILE_SIZE[0] + half] = 60
        return frame

    dt = float(engine.get_timestep())
    null_flag, fail_flag = base_env.DoneFlags.NULL.value, base_env.DoneFlags.FAIL.value
    failures = np.zeros(num_envs, dtype=int)
    video = []
    with torch.no_grad():
        obs, info = env.reset()
        for _ in range(30):
            shoot()  # renderer warm-up on the standing start
        for _ in range(int(round(VIDEO_SECONDS / dt))):
            obs, _, done, info = env.step(agent._decide_action(obs, info)[0])
            failures += (done == fail_flag).cpu().numpy()
            video.append(shoot())
            reset_ids = (done != null_flag).nonzero(as_tuple=False).flatten()
            if len(reset_ids) > 0:
                obs, info = env.reset(reset_ids)

    film_dir = exp_dir / "film"
    video = [frame for frame in video if frame is not None]
    write_video(video, int(round(1.0 / dt)), film_dir / f"grid_{key}.mp4", film_dir / f"grid_{key}.gif")
    print(f"촬영 완료: grid_{key}, 영상 {len(video)}프레임 (시작 시점 {[round(t, 3) for t in starts]}초, "
          f"실패 횟수 {failures.tolist()}) -> {film_dir}", flush=True)
    sys.stdout.flush()
    os._exit(0)  # Isaac Sim with cameras enabled does not shut down on a normal return


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("exp_dir", nargs="?", help="실험 폴더 (생략하면 가장 최근)")
    cli.add_argument("--variants", help="쉼표로 구분한 변형 폴더 이름 (기본: 폴더의 변형 전부)")
    cli.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    args = cli.parse_args()
    exp_dir = Path(args.exp_dir).resolve() if args.exp_dir else latest_experiment()
    if exp_dir is None:
        print(f"실험 결과가 없습니다: {HERE}", file=sys.stderr)
        return 1
    variants = ([key.strip() for key in args.variants.split(",") if key.strip()] if args.variants
                else [key for key, _, _ in load_variants(exp_dir)])
    return film_inside(exp_dir, variants[0]) if args.inside else launch(exp_dir, variants)


if __name__ == "__main__":
    raise SystemExit(main())
