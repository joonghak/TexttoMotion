#!/home/jong/isaaclab/.venv/bin/python
"""A video and close-up pictures of the style-walk policies, for judging the motion by eye (headless).

Usage on this computer:
    ./experiments/style_walk/film.py                                # most recent experiment
    ./experiments/style_walk/film.py experiments/style_walk/<폴더>
    ./experiments/style_walk/film.py <폴더> --variants base,strong
    ./experiments/style_walk/film.py <폴더> --episode 3                 # another episode: only the video, walk_ep3.mp4/.gif
    ./experiments/style_walk/film.py <폴더> --view front                # only the video, from the front: walk_front.mp4/.gif
    ./experiments/style_walk/film.py <폴더> --variants lean20,base,lean40 --colors 1,0,3 --name lean

Every variant walks from the start of the clip with its own policy. Results go to <폴더>/film/:
    walk.mp4, walk.gif               all variants in one world, seen from the side (1920x720, nothing drawn on it)
    walk_ep<N>.mp4, .gif, .json      the same for random-start episode N, and where in the clip each variant started
    walk_front.mp4, walk_quarter.mp4 the variants in a row across the picture, walking toward the camera (front) or seen
                                     from 40 degrees off their path (quarter); sideways motion shows here, not from the side
    side.png, front.png              one row per variant, one column per instant of a gait cycle
    <variant>_side.png, _front.png   the same pictures, larger
Colors as in play_compare.py, in the order of the folder's variants: 파랑, 초록, 주황, 빨강, 보라, 검정
(--colors picks them by number, 0-5, in the order of --variants). --name replaces "walk" in the file names.
Side view: the character walks to the right. Front view: it walks toward the camera.
In the video the variants start in single file, the slowest at the back (left) and nearest the
camera, each on a lane of its own so that they can pass each other; variants of equal speed
keep the folder's order. They stand further apart if the clip reaches far (a kick). The camera backs away as the group spreads out. If the speeds differ,
the video is the first 10 s (one episode from its start), so that the gaps opening between the
characters show the speed; a character whose episode fails starts again from its start. With
equal speeds the video is four gait cycles after 3 s of walking.
--episode N films a random-start episode instead: every character starts at its own random
instant of the clip (N seeds the draw), as in training and in quality_eval.py.
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
from play_compare import COLORS, build_camera, latest_experiment, recolor, render_frame, write_video  # noqa: E402
from run_style_walk import load_variants, read_scales, run_clip  # noqa: E402

DEVICE = "cuda:0"
RESOLUTION = (1920, 1080)
SPREAD = 8.0            # m between close-up characters (diagonal, so no one else is in the picture)
GROUP_ORIGIN = (-30.0, 44.0)  # m; where the group for the video starts (out of every close-up)
FILE_GAP = 1.5          # m between the characters of that group along the walking direction, at least
LANE_GAP = 0.6          # m between their lanes
WARMUP_STEPS = 90       # walk 3 s before filming
NUM_INSTANTS = 8        # close-ups per gait cycle
CAM_DIST, CAM_HEIGHT = 3.0, 0.9
CROP_W = 720            # close-ups keep the middle of the 1920-wide frame
RENDERS_PER_SHOT = 3    # the picture settles a few renders after the camera jumps
VIDEO_SIZE = (1920, 720)
VIDEO_SECONDS = 10.0    # length if the speeds differ (one episode)
VIDEO_CYCLES = 4        # length in gait cycles if the speeds are equal
VIDEO_HFOV = 60.0       # deg
VIDEO_MIN_DIST = 7.5    # m; nearer than this a character does not fit the height of the frame
VIDEO_MARGIN = 1.6      # m kept free left and right of the group
VIDEO_PITCH = 6.0       # deg the camera looks down, so that the lanes read as depth
VIDEO_SMOOTH = 0.3      # share of the way the camera moves to its goal per step
ABREAST_GAP = 1.4       # m between the characters across the picture in the front and quarter views
ABREAST_MIN_DIST = 5.2  # m; those views show few characters, so the camera may come nearer (a character is 70% of the height)
# view -> deg between the walking direction and the direction from the group to the camera
VIEW_AZIMUTH = {"side": 90.0, "quarter": 40.0, "front": 0.0}


def launch(exp_dir: Path, variants, episode: int, view: str, color_ids, name: str) -> int:
    missing = [key for key in variants if not (exp_dir / key / "train" / "model.pt").exists()]
    if missing:
        print(f"학습된 모델이 없습니다: {', '.join(missing)} ({exp_dir})", file=sys.stderr)
        return 1
    os.environ.setdefault("DISPLAY", play_motion.DEFAULT_DISPLAY)
    os.environ.setdefault("XAUTHORITY", play_motion.DEFAULT_XAUTHORITY)
    (exp_dir / "film").mkdir(exist_ok=True)
    args = [exp_dir, "--inside", "--variants", ",".join(variants), "--episode", episode, "--view", view, "--name", name]
    if color_ids:
        args += ["--colors", ",".join(str(c) for c in color_ids)]
    return tft.run_in_isaaclab(args, log_file=exp_dir / "film" / "console.log", script=Path(__file__).resolve())


def reference_reach(env_config) -> float:
    """How far (m) any body part gets from the pelvis over the ground in the reference clip."""
    import anim.mjcf_char_model as mjcf_char_model
    import anim.motion_lib as motion_lib
    import torch

    kin = mjcf_char_model.MJCFCharModel("cpu")
    kin.load(env_config["char_file"])
    lib = motion_lib.MotionLib(motion_file=env_config["motion_file"], kin_char_model=kin, device="cpu")
    ids = torch.zeros(120, dtype=torch.long)
    times = torch.arange(120, dtype=torch.float) * (float(lib.get_motion_length(ids[:1])[0]) / 120)
    root_pos, root_rot, _, _, joint_rot, _ = lib.calc_motion_frame(ids, times)
    body_pos, _ = kin.forward_kinematics(root_pos, root_rot, joint_rot)
    return float(torch.linalg.vector_norm(body_pos[:, :, 0:2] - root_pos[:, None, 0:2], dim=-1).max())


def film_inside(exp_dir: Path, variants, episode: int, view: str, color_ids, name: str) -> int:
    """Runs under Isaac Lab from the MimicKit directory. episode 0 from the side: from the clip start, with the close-ups."""
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
    from PIL import Image, ImageDraw

    num_variants = len(variants)
    num_envs = 2 * num_variants
    all_keys = [key for key, _, _ in load_variants(exp_dir)]
    colors = [COLORS[all_keys.index(key) % len(COLORS)] if key in all_keys else COLORS[i % len(COLORS)]
              for i, key in enumerate(variants)]
    if color_ids:
        colors = [COLORS[c % len(COLORS)] for c in color_ids]
    runs = [exp_dir / key for key in variants]
    scales = [read_scales(run) for run in runs]
    speeds = [scale["speed"] * scale["cadence"] for scale in scales]  # ground speed, in units of the reference's
    by_speed = sorted(range(num_variants), key=lambda v: speeds[v])
    place = [by_speed.index(v) for v in range(num_variants)]  # faster characters start further ahead
    mixed_speeds = max(speeds) > min(speeds)

    config_dir = runs[0] / "config"
    env_config, engine_config = env_builder.load_configs(str(config_dir / "env_play.yaml"), str(config_dir / "engine.yaml"))
    file_gap = max(FILE_GAP, 2.0 * reference_reach(env_config) + 0.3)  # neighbours must not reach into each other

    abreast = view != "side"
    azimuth = math.radians(VIEW_AZIMUTH[view])
    # Front and quarter views: the characters stand in a row across the picture, all as far from the camera.
    group_gap = (ABREAST_GAP * math.sin(azimuth), ABREAST_GAP * math.cos(azimuth)) if abreast else (file_gap, LANE_GAP)

    def layout(self, n):
        """Envs 0..V-1: close-up characters on a diagonal. Envs V..2V-1: the group, in file and one lane each
        (side view) or in a row facing the camera (front and quarter views)."""
        slot = torch.tensor(place + place, device=self._device, dtype=torch.float)
        closeup = torch.arange(n, device=self._device) < num_variants
        offsets = torch.zeros([n, 2], device=self._device, dtype=torch.float)
        offsets[:, 0] = torch.where(closeup, slot * SPREAD, GROUP_ORIGIN[0] + slot * group_gap[0])
        offsets[:, 1] = torch.where(closeup, slot * SPREAD, GROUP_ORIGIN[1] + slot * group_gap[1])
        return offsets

    isaac_lab_engine.IsaacLabEngine._compute_env_offsets = layout
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=num_envs,
                                        device=DEVICE, visualize=False, record_video=True)
    engine, char_id = env._engine, env._get_char_id()
    recolor(engine, char_id, colors * 2)
    agents = []
    for run in runs:
        agent = agent_builder.build_agent(str(run / "config" / "agent.yaml"), env, DEVICE)
        agent.load(str(run / "train" / "model.pt"))
        agent.eval()
        agent.set_mode(base_agent.AgentMode.TEST)
        agents.append(agent)
    engine.stop_video_recording()  # test mode starts recording every step; frames are grabbed manually here
    engine._video_recorder._resolution = RESOLUTION
    # DLAA: anti-aliasing at the full resolution. The default (DLSS) renders at about half of it and
    # scales up, which smears the grid lines and the shadows.
    carb.settings.get_settings().set("/rtx/post/aa/op", 4)
    env_ids_of = [torch.tensor([v, v + num_variants], device=DEVICE) for v in range(num_variants)]
    for ids, scale in zip(env_ids_of, scales):  # each character follows the reference with its own step length and rhythm
        env._speed_scale[ids] = scale["speed"]
        env._cadence_scale[ids] = scale["cadence"]
        env._weave_amp[ids] = scale.get("weave", 0.0)

    def act(obs, info):
        actions = None
        for agent, ids in zip(agents, env_ids_of):
            action = agent._decide_action(obs[ids], info)[0]
            if actions is None:
                actions = torch.zeros([num_envs, action.shape[-1]], device=DEVICE, dtype=action.dtype)
            actions[ids] = action
        return actions

    def world_xy(env_ids):
        """Root positions in env-0 coordinates (the frame of the engine's camera)."""
        return (engine.get_root_pos(char_id)[env_ids, 0:2] + engine._env_offsets[env_ids]
                - engine._env_offsets[0]).cpu().numpy()

    def shoot(cam_pos, target):
        """RGB frame of RESOLUTION from cam_pos looking at target, or None while the renderer warms up."""
        return render_frame(engine, cam_pos, target, RENDERS_PER_SHOT)

    def shoot_closeup(v, view_name):
        xy = world_xy(v)
        target = np.array([xy[0], xy[1], CAM_HEIGHT])
        delta = np.array([0.0, -CAM_DIST, 0.1]) if view_name == "side" else np.array([CAM_DIST, 0.0, 0.1])
        frame = shoot(target + delta, target)
        if frame is None:
            return None
        left = (frame.shape[1] - CROP_W) // 2
        return frame[:, left:left + CROP_W]

    look, read = build_camera(engine, "film_camera", VIDEO_SIZE, VIDEO_HFOV)  # the engine's camera jumps between the close-ups
    group_ids = torch.arange(num_variants, num_envs, device=DEVICE)  # env V + v is variant v's character in the video
    lane_y = GROUP_ORIGIN[1] + 0.5 * (num_variants - 1) * LANE_GAP
    view_span = None  # [centre, width] of the stretch of track that the side view shows
    reach_max = -math.inf
    spot = None  # [x, y, width] of the group as the front and quarter views frame it

    def shoot_abreast():
        """The group from the front or from 40 degrees off its path, or None while the renderer warms up."""
        nonlocal spot
        xy = (engine.get_root_pos(char_id)[group_ids, 0:2] + engine._env_offsets[group_ids]).cpu().numpy()
        across = xy @ np.array([math.sin(azimuth), math.cos(azimuth)])  # along the picture's width
        goal = np.array([xy[:, 0].mean(), xy[:, 1].mean(), across.max() - across.min()])
        spot = goal if spot is None else spot + VIDEO_SMOOTH * (goal - spot)
        dist = max(ABREAST_MIN_DIST, 0.5 * (spot[2] + 2.0 * VIDEO_MARGIN) / math.tan(0.5 * math.radians(VIDEO_HFOV)))
        pitch = math.radians(VIDEO_PITCH)
        target = np.array([spot[0], spot[1], 0.9])
        look(target + dist * np.array([math.cos(azimuth) * math.cos(pitch), -math.sin(azimuth) * math.cos(pitch),
                                       math.sin(pitch)]), target)
        engine.get_sim().render()
        return read()

    def shoot_video():
        """The whole group from the side, or None while the renderer warms up."""
        nonlocal view_span, reach_max
        if abreast:
            return shoot_abreast()
        x = (engine.get_root_pos(char_id)[group_ids, 0] + engine._env_offsets[group_ids, 0]).cpu().numpy()
        # The far end only moves forward: a character thrown back to its start must not make the camera lurch.
        reach_max = max(reach_max, x.max())
        goal = np.array([0.5 * (x.min() + reach_max), reach_max - x.min()])
        view_span = goal if view_span is None else view_span + VIDEO_SMOOTH * (goal - view_span)
        dist = max(VIDEO_MIN_DIST, 0.5 * (view_span[1] + 2.0 * VIDEO_MARGIN) / math.tan(0.5 * math.radians(VIDEO_HFOV)))
        pitch = math.radians(VIDEO_PITCH)
        target = np.array([view_span[0], lane_y, 0.9])
        look(target + dist * np.array([0.0, -math.cos(pitch), math.sin(pitch)]), target)
        engine.get_sim().render()
        return read()

    dt = float(engine.get_timestep())
    cycle = int(round(float(env._motion_lib.get_motion_length(torch.zeros(1, dtype=torch.long, device=DEVICE))[0]) / dt))
    # A clip that does not loop (a chain of actions, experiments/chain) is filmed once from its start to its end.
    once = "humanoid_chain_" in str(env_config.get("motion_file", ""))  # the kick's single clip keeps the usual film
    whole_episode = mixed_speeds or episode > 0 or once
    video_start = 0 if whole_episode else WARMUP_STEPS
    video_steps = int(round(VIDEO_SECONDS / dt)) if whole_episode else VIDEO_CYCLES * cycle
    if (once):
        video_steps = min(video_steps, cycle - 1)
    closeup_start = WARMUP_STEPS + video_steps
    video_only = episode > 0 or abreast
    instants = [] if video_only else [closeup_start + int(round(i * cycle / NUM_INSTANTS)) for i in range(NUM_INSTANTS)]
    null_flag, fail_flag = base_env.DoneFlags.NULL.value, base_env.DoneFlags.FAIL.value
    closeups = {(v, view_name): [] for v in range(num_variants) for view_name in ("side", "front")}
    failures = np.zeros(num_variants, dtype=int)  # in the video
    video = []
    with torch.no_grad():
        env._rand_reset = episode > 0
        torch.manual_seed(episode)  # the start instants of a random-start episode
        obs, info = env.reset()
        start_times = env._motion_time_offsets[group_ids].tolist()  # s into the clip
        for _ in range(30):
            shoot_video()  # renderer warm-up on the standing start
        for step in range(video_start + video_steps if video_only else closeup_start + cycle):
            obs, _, done, info = env.step(act(obs, info))
            if video_start <= step < video_start + video_steps:
                if step == video_start and video_start > 0:
                    # The camera starts on the group, not where the group stood before the warm-up walk.
                    view_span, spot, reach_max = None, None, -math.inf
                    for _ in range(RENDERS_PER_SHOT):
                        shoot_video()
                failures += (done[group_ids] == fail_flag).cpu().numpy()
                video.append(shoot_video())
            if step == video_start + video_steps and not video_only:
                for _ in range(10):
                    shoot_closeup(0, "side")  # warm-up of the engine's camera, used from here on
            if step in instants:
                for (v, view_name), tiles in closeups.items():
                    tiles.append(shoot_closeup(v, view_name))
            reset_ids = (done != null_flag).nonzero(as_tuple=False).flatten()
            if len(reset_ids) > 0:
                obs, info = env.reset(reset_ids)

    film_dir = exp_dir / "film"
    video = [frame for frame in video if frame is not None]
    name = name + ("" if view == "side" else f"_{view}") + ("" if episode == 0 else f"_ep{episode}")
    if video:
        write_video(video, int(round(1.0 / dt)), film_dir / f"{name}.mp4", film_dir / f"{name}.gif")
    if episode > 0:
        # film_grid.py starts its characters at the same instants
        (film_dir / f"{name}.json").write_text(json.dumps({"start_time_s": dict(zip(variants, start_times))}, indent=2))
    if video_only:
        print(f"촬영 완료: {name}, 영상 {len(video)}프레임 (영상 중 실패 횟수 {dict(zip(variants, failures.tolist()))}, "
              f"시작 시점 {dict(zip(variants, [round(x, 3) for x in start_times]))}초) -> {film_dir}", flush=True)
        sys.stdout.flush()
        os._exit(0)

    def sheet(rows, tile_size, labels):
        """rows: lists of frames; one sheet row per list, labelled at its left edge."""
        width, height = tile_size
        image = Image.new("RGB", (width * max(len(row) for row in rows), height * len(rows)))
        draw = ImageDraw.Draw(image)
        for r, row in enumerate(rows):
            for c, frame in enumerate(row):
                if frame is not None:
                    image.paste(Image.fromarray(frame).resize(tile_size, Image.LANCZOS), (c * width, r * height))
            draw.text((6, r * height + 4), labels[r], fill=(255, 255, 255))
        return image

    seconds = ["t={:.2f}s".format((step - closeup_start) * dt) for step in instants]
    for view_name in ("side", "front"):
        rows = [closeups[(v, view_name)] for v in range(num_variants)]
        sheet(rows, (200, 300), list(variants)).save(film_dir / (f"{view_name}.png" if name == "walk" else f"{name}_{view_name}.png"))
        for v, key in enumerate(variants):
            half = (NUM_INSTANTS + 1) // 2
            sheet([rows[v][:half], rows[v][half:]], (400, 600),
                  [f"{key} {view_name} {seconds[0]}..", f"{key} {view_name} {seconds[half]}.."]).save(
                      film_dir / f"{key}_{view_name}.png")

    print(f"촬영 완료: 근접 {NUM_INSTANTS}장 × {num_variants}개 × 2방향, 영상 {len(video)}프레임 "
          f"(영상 중 실패 횟수 {dict(zip(variants, failures.tolist()))}) -> {film_dir}", flush=True)
    sys.stdout.flush()
    os._exit(0)  # Isaac Sim with cameras enabled does not shut down on a normal return


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("exp_dir", nargs="?", help="실험 폴더 (생략하면 가장 최근)")
    cli.add_argument("--variants", help="쉼표로 구분한 변형 폴더 이름 (기본: 폴더의 변형 전부)")
    cli.add_argument("--episode", type=int, default=0, metavar="N",
                     help="무작위 시점에서 시작하는 에피소드 N번을 영상으로만 저장 (walk_epN.mp4/.gif)")
    cli.add_argument("--view", choices=tuple(VIEW_AZIMUTH), default="side",
                     help="영상을 찍는 방향: side(옆, 기본), front(정면), quarter(비스듬히). front와 quarter는 영상만 저장")
    cli.add_argument("--colors", help="쉼표로 구분한 색 번호, --variants 순서대로 (0 파랑, 1 초록, 2 주황, 3 빨강, 4 보라, 5 검정)")
    cli.add_argument("--name", default="walk", help="저장할 파일 이름의 앞부분 (기본 walk)")
    cli.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    args = cli.parse_args()
    exp_dir = Path(args.exp_dir).resolve() if args.exp_dir else latest_experiment()
    if exp_dir is None:
        print(f"실험 결과가 없습니다: {HERE}", file=sys.stderr)
        return 1
    variants = ([key.strip() for key in args.variants.split(",") if key.strip()] if args.variants
                else [key for key, _, _ in load_variants(exp_dir)])
    clips = {run_clip(exp_dir / key) for key in variants}
    if len(clips) > 1:  # one simulation loads one reference clip for every character
        print("참조 모션이 다른 변형은 따로 실행하세요: " + ", ".join(sorted(clips)), file=sys.stderr)
        return 1
    color_ids = [int(c) for c in args.colors.split(",")] if args.colors else None
    if color_ids and len(color_ids) != len(variants):
        print("--colors 의 개수가 변형 수와 다릅니다", file=sys.stderr)
        return 1
    if args.inside:
        return film_inside(exp_dir, variants, args.episode, args.view, color_ids, args.name)
    return launch(exp_dir, variants, args.episode, args.view, color_ids, args.name)


if __name__ == "__main__":
    raise SystemExit(main())
