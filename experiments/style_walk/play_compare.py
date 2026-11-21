#!/home/jong/isaaclab/.venv/bin/python
"""Show the variants of one experiment side by side in one Isaac Lab viewer.

Usage on this computer:
    ./experiments/style_walk/play_compare.py                                  # most recent experiment
    ./experiments/style_walk/play_compare.py experiments/style_walk/<폴더>
    ./experiments/style_walk/play_compare.py <폴더> --record                  # no window: save the same scene as a video

Colors follow the order of the folder's variants (printed at start): 파랑, 초록, 주황, 빨강, 보라, 검정.
The characters stand in a row across the walking direction (slowest nearest the camera)
and start together; every 10 s they restart. The camera follows the middle of the group
(it keeps any angle you set with Alt+drag). Close the window or press Ctrl+C to stop.
Each character is driven by its own trained policy inside one simulation.
--record [초] films one run from the start (default 10 s) into <폴더>/film/compare.mp4
and compare.gif; the camera backs away as the characters spread out.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import play_motion  # noqa: E402
import train_from_text as tft  # noqa: E402
from run_style_walk import load_variants, read_scales  # noqa: E402

COLORS = [(0.2, 0.25, 0.7), (0.15, 0.6, 0.25), (0.95, 0.55, 0.1), (0.8, 0.12, 0.12), (0.5, 0.12, 0.65), (0.06, 0.06, 0.06)]
COLOR_NAMES = ["파랑", "초록", "주황", "빨강", "보라", "검정"]
SPACING = 1.5  # m between neighbouring characters
DEVICE = "cuda:0"
CAMERA_OFFSET = (4.0, -5.5, 1.0)   # viewer camera, from the middle of the group
RECORD_OFFSET = (3.4, -4.7, 1.4)   # recording camera at the start; it backs away by RECORD_ZOOM per metre of spread
RECORD_ZOOM = 1.0 / 12.0
RECORD_RESOLUTION = (1920, 1080)


def recolor(engine, obj_id, colors):
    """Give each env's copy of an object its own colour.

    The engine builds env 0 and clones it, so per-env colours passed at creation are lost.
    """
    from pxr import Gf, Usd, UsdShade

    for env_id, color in enumerate(colors):
        root = engine._stage.GetPrimAtPath("/World/envs/env_{}/obj_{}".format(env_id, obj_id))
        for prim in Usd.PrimRange(root):
            if prim.IsA(UsdShade.Shader):
                attr = prim.GetAttribute("inputs:diffuseColor")
                if attr:
                    attr.Set(Gf.Vec3f(*color))


def latest_experiment():
    runs = sorted(path for path in HERE.iterdir() if path.is_dir() and path.name[:2] == "20")
    return runs[-1] if runs else None


def render_frame(engine, cam_pos, target, renders=3):
    """RGB frame [H, W, 3] of the headless renderer from cam_pos looking at target, or None while it warms up.

    The env has to be built with record_video=True. The picture settles a few renders after the camera jumps.
    """
    import numpy as np

    recorder = engine._video_recorder
    recorder._build_annotator()
    engine.set_camera_pose(np.asarray(cam_pos, dtype=np.float64), np.asarray(target, dtype=np.float64))
    for _ in range(renders):
        engine.get_sim().render()
    data = recorder._annotator.get_data()
    if data is None or data.size == 0:
        return None
    return np.frombuffer(data, dtype=np.uint8).reshape(*data.shape)[:, :, :3].copy()


def build_camera(engine, name, size, hfov_deg):
    """A camera of its own with a picture of size (the engine's own camera can only be in one place).

    Returns look(eye, target), which moves it (world coordinates, numpy), and read(), which gives the RGB
    frame of the last render, or None while the renderer warms up. The env has to be built with record_video=True.
    """
    import math

    import numpy as np
    import omni.replicator.core as rep
    from pxr import Gf, UsdGeom

    path, aperture = "/World/" + name, 20.955
    camera = UsdGeom.Camera.Define(engine._stage, path)
    camera.GetHorizontalApertureAttr().Set(aperture)
    camera.GetVerticalApertureAttr().Set(aperture * size[1] / size[0])
    camera.GetFocalLengthAttr().Set(0.5 * aperture / math.tan(0.5 * math.radians(hfov_deg)))
    camera.GetClippingRangeAttr().Set(Gf.Vec2f(0.1, 1000.0))
    xform = UsdGeom.Xformable(camera).AddTransformOp()
    annotator = rep.AnnotatorRegistry.get_annotator("rgb", device="cpu")
    annotator.attach([rep.create.render_product(path, size)])

    def look(eye, target):
        view = Gf.Matrix4d().SetLookAt(Gf.Vec3d(*eye.tolist()), Gf.Vec3d(*target.tolist()), Gf.Vec3d(0.0, 0.0, 1.0))
        xform.Set(view.GetInverse())

    def read():
        data = annotator.get_data()
        if data is None or data.size == 0:
            return None
        return np.frombuffer(data, dtype=np.uint8).reshape(*data.shape)[:, :, :3].copy()

    return look, read


def write_video(frames, fps, mp4_file, gif_file=None, gif_width=960, gif_fps=12.5):
    """Save RGB frames as an mp4 (near lossless) and, optionally, a GIF gif_width pixels wide at gif_fps.

    A GIF times its frames in hundredths of a second: 12.5 fps (0.08 s) plays at the true speed, 15 fps would not.
    """
    import subprocess

    import imageio_ffmpeg
    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

    ImageSequenceClip(frames, fps=fps).write_videofile(str(mp4_file), codec="libx264", preset="slow",
                                                       ffmpeg_params=["-crf", "17"], logger=None)
    if gif_file is not None:
        # One palette for the whole clip, taken from the clip: PIL's fixed palette shows as colour bands.
        filters = (f"fps={gif_fps},scale={gif_width}:-2:flags=lanczos,split[a][b];"
                   "[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle")
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(mp4_file),
                        "-vf", filters, "-loop", "0", str(gif_file)], check=True)


def launch(exp_dir: Path, smoke_steps: int, record_s: float) -> int:
    """Check the runs, then start this script again inside the Isaac Lab environment."""
    variants = load_variants(exp_dir)
    missing = [key for key, _, _ in variants if not (exp_dir / key / "train" / "model.pt").exists()]
    if missing:
        print(f"학습된 모델이 없습니다: {', '.join(missing)} ({exp_dir})", file=sys.stderr)
        return 1
    for (key, label, _), color in zip(variants, COLOR_NAMES):
        print(f"{color}: {label} ({key})", flush=True)
    os.environ.setdefault("DISPLAY", play_motion.DEFAULT_DISPLAY)
    os.environ.setdefault("XAUTHORITY", play_motion.DEFAULT_XAUTHORITY)
    args = [exp_dir, "--inside"] + (["--smoke", smoke_steps] if smoke_steps else [])
    if record_s:
        (exp_dir / "film").mkdir(exist_ok=True)
        args += ["--record", record_s]
    try:
        return tft.run_in_isaaclab(args, script=Path(__file__).resolve())
    except KeyboardInterrupt:
        return 130


def play_inside(exp_dir: Path, smoke_steps: int, record_s: float) -> int:
    """Runs under Isaac Lab from the MimicKit directory."""
    sys.path.insert(0, str(tft.MIMICKIT / "mimickit"))
    import envs.env_builder as env_builder
    import learning.agent_builder as agent_builder
    import envs.base_env as base_env
    import envs.text_reward_env as text_reward_env
    import engines.isaac_lab_engine as isaac_lab_engine
    import learning.base_agent as base_agent
    import util.camera as camera
    import util.mp_util as mp_util
    import numpy as np
    import torch

    runs = [exp_dir / key for key, _, _ in load_variants(exp_dir)]
    scales = [read_scales(run) for run in runs]
    speeds = [scale["speed"] * scale["cadence"] for scale in scales]  # ground speed, in units of the reference's
    by_speed = sorted(range(len(runs)), key=lambda index: speeds[index])
    lane = [by_speed.index(index) for index in range(len(runs))]  # slowest nearest the camera: they fan out, never cross

    def row_offsets(self, num_envs):
        """All characters in one row across the walking (+x) direction."""
        offsets = torch.zeros([num_envs, 2], device=self._device, dtype=torch.float)
        offsets[:, 1] = (torch.tensor(lane, device=self._device, dtype=torch.float) - (num_envs - 1) / 2) * SPACING
        return offsets

    isaac_lab_engine.IsaacLabEngine._compute_env_offsets = row_offsets

    class GroupCamera(camera.Camera):
        """Track mode that follows the centre of all characters instead of env 0."""

        def update(self):
            cam_pos, cam_dir = self._engine.get_camera_pos(), self._engine.get_camera_dir()
            prev_delta = self._target - self._pos
            prev_dist = np.linalg.norm(prev_delta)
            if not np.allclose(self._pos, cam_pos, atol=1e-5):
                cam_delta = cam_pos - self._target
            elif not np.allclose(prev_delta / prev_dist, cam_dir, atol=1e-5):
                cam_delta = -prev_dist * cam_dir
            else:
                cam_delta = cam_pos - self._target
            center = group_center()
            new_target = np.array([center[0], center[1], self._target[2]])
            self.lookat(new_target + cam_delta, new_target)

    config_dir = runs[0] / "config"
    env_config, engine_config = env_builder.load_configs(str(config_dir / "env_play.yaml"), str(config_dir / "engine.yaml"))
    mp_util.init(0, 1, DEVICE, int(np.random.randint(6000, 7000)))
    visualize = not smoke_steps and not record_s
    env = text_reward_env.TextRewardEnv(env_config=env_config, engine_config=engine_config, num_envs=len(runs),
                                        device=DEVICE, visualize=visualize, record_video=bool(record_s))
    engine, char_id = env._engine, env._get_char_id()
    recolor(engine, char_id, COLORS[:len(runs)])
    # each character follows the reference with its own step length and rhythm
    env._speed_scale[:] = torch.tensor([scale["speed"] for scale in scales], device=DEVICE)
    env._cadence_scale[:] = torch.tensor([scale["cadence"] for scale in scales], device=DEVICE)
    env._weave_amp[:] = torch.tensor([scale.get("weave", 0.0) for scale in scales], device=DEVICE)

    def group_center():
        """Mean root position in env-0 coordinates (the camera's frame)."""
        world_xy = engine.get_root_pos(char_id)[:, 0:2] + engine._env_offsets
        return (world_xy.mean(dim=0) - engine._env_offsets[0]).cpu().numpy()

    agents = []
    for run in runs:
        agent = agent_builder.build_agent(str(run / "config" / "agent.yaml"), env, DEVICE)
        agent.load(str(run / "train" / "model.pt"))
        agent.eval()
        agent.set_mode(base_agent.AgentMode.TEST)
        agents.append(agent)

    obs, info = env.reset()
    if visualize:
        center = group_center()
        target = np.array([center[0], center[1], 0.9])
        env._camera = GroupCamera(mode=camera.CameraMode.track, engine=engine,
                                  pos=target + np.array(CAMERA_OFFSET), target=target)
    if record_s:
        engine.stop_video_recording()  # test mode records every step; the frames are grabbed here instead
        engine._video_recorder._resolution = RECORD_RESOLUTION

    def film():
        """The viewer's view of the whole group, backing away as the characters spread along the track."""
        xy = (engine.get_root_pos(char_id)[:, 0:2] + engine._env_offsets - engine._env_offsets[0]).cpu().numpy()
        low, high = xy.min(axis=0), xy.max(axis=0)
        target = np.array([0.5 * (low[0] + high[0]), 0.5 * (low[1] + high[1]), 0.9])
        zoom = 1.0 + RECORD_ZOOM * (high[0] - low[0])
        return render_frame(engine, target + zoom * np.array(RECORD_OFFSET), target)

    def running():
        launcher = getattr(engine, "_app_launcher", None)
        return launcher is None or launcher.app.is_running()

    dt = float(engine.get_timestep())
    record_steps = int(round(record_s / dt))
    frames = []
    for _ in range(30 if record_s else 0):
        film()  # renderer warm-up on the standing start
    null_flag, steps = base_env.DoneFlags.NULL.value, 0
    with torch.no_grad():
        while running() and (not smoke_steps or steps < smoke_steps) and (not record_s or steps < record_steps):
            actions = torch.cat([agent._decide_action(obs[i:i + 1], info)[0] for i, agent in enumerate(agents)], dim=0)
            obs, _, done, info = env.step(actions)
            if record_s:
                frames.append(film())
            reset_ids = (done != null_flag).nonzero(as_tuple=False).flatten()
            if len(reset_ids) > 0:
                obs, info = env.reset(reset_ids)
            steps += 1
    if smoke_steps:
        print(f"smoke OK: {steps} steps, root x = {engine.get_root_pos(char_id)[:, 0].tolist()}", flush=True)
    if record_s:
        frames = [frame for frame in frames if frame is not None]
        video = exp_dir / "film" / "compare.mp4"
        write_video(frames, int(round(1.0 / dt)), video, video.with_suffix(".gif"))
        print(f"녹화 완료: {len(frames)}프레임 ({len(frames) * dt:.1f}초) -> {video}", flush=True)
        sys.stdout.flush()
        os._exit(0)  # Isaac Sim with cameras enabled does not shut down on a normal return
    return 0


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("exp_dir", nargs="?", help="실험 폴더 (생략하면 가장 최근)")
    cli.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    cli.add_argument("--smoke", type=int, default=0, help=argparse.SUPPRESS)
    cli.add_argument("--record", type=float, nargs="?", const=10.0, default=0.0, metavar="초",
                     help="창 없이 같은 장면을 영상으로 저장 (기본 10초)")
    args = cli.parse_args()

    exp_dir = Path(args.exp_dir).resolve() if args.exp_dir else latest_experiment()
    if exp_dir is None:
        print(f"실험 결과가 없습니다: {HERE}", file=sys.stderr)
        return 1
    if args.inside:
        return play_inside(exp_dir, args.smoke, args.record)
    return launch(exp_dir, args.smoke, args.record)


if __name__ == "__main__":
    raise SystemExit(main())
