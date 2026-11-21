#!/home/jong/isaaclab/.venv/bin/python
"""Natural-language command -> DeepMimic policy trained on Isaac Lab, saved to outputs/.

Usage on this computer:
    ./train_from_text.py "5초동안 전방으로 천천히 스핀킥하는 모델을 만들어"
    ./train_from_text.py --num-envs 512 "왼쪽으로 빠르게 10초 동안 걸어"

Pipeline:
1. motion_parser.py (Qwen, separate process so its GPU memory is freed) turns the
   command into {"action", "direction", "speed", "duration"}.
2. A reference clip is built from the MimicKit motion pool:
   - action picks the clip (walk, run, kick, spinkick),
   - direction rotates the whole clip about the vertical axis (counterclockwise),
   - speed changes the playback rate: 0.5 is the original clip,
     0 and 1 are SPEED_RATE_RANGE times slower/faster (log scale),
   - duration sets the clip length. Walk/run use the exact time; kick/spinkick
     are rounded to whole repetitions (at least one). Looping clips (walk, run,
     spinkick) repeat like MimicKit's WRAP mode; the kick continues from its end
     position and heading.
3. MimicKit trains DeepMimic (PPO) headless for TRAIN_ITERS iterations (--iters).
4. Results go to outputs/<time>_<action>/ (--out-root, --run-name); replay them
   with ./play_motion.py.

Run folder contents:
    summary.json          command, parsed values, reference details, final log row
    reference.pkl         generated MimicKit motion clip (CLAMP loop mode)
    config/               env (train and play), agent, and engine configs
    train/                MimicKit output: model.pt, log.txt, config copies
    train_console.log     full training console output
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MIMICKIT = ROOT / "MimicKit"
PARSER = ROOT / "motion_parser.py"
OUTPUT_ROOT = ROOT / "outputs"
ISAACLAB_ACTIVATE = Path("/home/jong/isaaclab/activate.sh")

BASE_ENV_CONFIG = MIMICKIT / "data/envs/deepmimic_humanoid_env.yaml"
BASE_AGENT_CONFIG = MIMICKIT / "data/agents/deepmimic_humanoid_ppo_agent.yaml"
ENGINE_CONFIG = MIMICKIT / "data/engines/isaac_lab_engine.yaml"
CLIP_DIR = MIMICKIT / "data/motions/humanoid"
CLIPS = {
    "walk": "humanoid_walk.pkl",
    "run": "humanoid_run.pkl",
    "kick": "humanoid_kick.pkl",
    "spinkick": "humanoid_spinkick.pkl",
}
REPEATED_SKILLS = ("kick", "spinkick")
SPEED_RATE_RANGE = 1.5
TRAIN_ITERS = 1000
DEFAULT_NUM_ENVS = 1024
RAND_SEED = 42


def run_in_isaaclab(mimickit_args, log_file=None, script="mimickit/run.py") -> int:
    """Run a MimicKit script (run.py by default) inside the Isaac Lab environment.

    Same as the manual commands: activate.sh (which also clears ROS variables that
    conflict with Isaac Sim), then the script from the MimicKit directory.
    Output is streamed to the terminal and, if given, copied to log_file.
    """
    command = (f"source {shlex.quote(str(ISAACLAB_ACTIVATE))} >/dev/null && "
               f"cd {shlex.quote(str(MIMICKIT))} && "
               f"exec python -u {shlex.quote(str(script))} {shlex.join(str(arg) for arg in mimickit_args)}")
    if log_file is None:
        return subprocess.run(["bash", "-c", command]).returncode
    with open(log_file, "w", encoding="utf-8") as log, subprocess.Popen(
            ["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, errors="replace") as proc:
        for line in proc.stdout:
            sys.stdout.write(line)
            log.write(line)
        return proc.wait()


def parse_command(text: str) -> dict:
    """Run motion_parser.py; its stderr (loading, rejections) goes straight to the terminal."""
    proc = subprocess.run([sys.executable, str(PARSER), "--offline", text],
                          stdout=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return json.loads(proc.stdout)


def _rotate_xy(xy, angle: float):
    import torch

    c, s = math.cos(angle), math.sin(angle)
    return torch.stack([c * xy[..., 0] - s * xy[..., 1], s * xy[..., 0] + c * xy[..., 1]], dim=-1)


def build_reference(parsed: dict, out_file: Path) -> dict:
    """Write the reference clip for the parsed command and return its description."""
    import numpy as np
    import torch

    sys.path.insert(0, str(MIMICKIT / "mimickit"))
    import anim.motion as motion
    import util.torch_util as torch_util

    action = parsed["action"]
    clip = motion.load_motion(str(CLIP_DIR / CLIPS[action]))
    # MimicKit reads NaN rotations (the walk clip's neck) as identity; store that explicitly.
    frames = torch.from_numpy(np.nan_to_num(clip.frames, nan=0.0)).float()
    num_frames = frames.shape[0]

    rate = SPEED_RATE_RANGE ** ((parsed["speed"] - 0.5) / 0.5)
    fps = float(clip.fps) * rate
    rep_time = (num_frames - 1) / fps
    if action in REPEATED_SKILLS:
        reps = max(1, round(parsed["duration"] / rep_time))
        keep = reps * (num_frames - 1) + 1
    else:
        reps = max(1, math.ceil(parsed["duration"] / rep_time))
        keep = max(2, round(parsed["duration"] * fps) + 1)

    root_pos = frames[:, 0:3]
    root_rot = torch_util.exp_map_to_quat(frames[:, 3:6])
    heading = torch_util.calc_heading(root_rot)
    # Looping clips repeat like MimicKit's WRAP mode: position carries over, heading does not
    # (their end-to-start heading residual, e.g. -5.3 deg per run cycle, would bend the path).
    # The non-looping kick really turns about 146 deg, so its repetitions continue from there.
    heading_change = 0.0 if clip.loop_mode == motion.LoopMode.WRAP else float(heading[-1] - heading[0])
    local_xy = root_pos[:, 0:2] - root_pos[0, 0:2]
    step_xy = local_xy[-1]

    yaw = 2.0 * math.pi * parsed["direction"]
    offset = root_pos[0, 0:2].clone()
    pieces = []
    for rep in range(reps):
        yaw_quat = torch.tensor([0.0, 0.0, math.sin(yaw / 2), math.cos(yaw / 2)]).expand_as(root_rot)
        piece = frames.clone()
        piece[:, 0:2] = _rotate_xy(local_xy, yaw) + offset
        piece[:, 3:6] = torch_util.quat_to_exp_map(torch_util.quat_mul(yaw_quat, root_rot))
        # The first frame of a repetition is the same instant as the previous last frame.
        pieces.append(piece if rep == 0 else piece[1:])
        offset = offset + _rotate_xy(step_xy, yaw)
        yaw += heading_change
    reference = torch.cat(pieces)[:keep]

    motion.Motion(loop_mode=motion.LoopMode.CLAMP, fps=fps, frames=reference.numpy()).save(str(out_file))
    return {
        "clip": str(CLIP_DIR / CLIPS[action]),
        "file": str(out_file),
        "yaw_deg": 360.0 * parsed["direction"],
        "playback_rate": rate,
        "fps": fps,
        "repetitions": reps if action in REPEATED_SKILLS else None,
        "duration_s": (keep - 1) / fps,
        "frames": keep,
    }


def write_configs(config_dir: Path, reference: dict) -> dict:
    import yaml

    config_dir.mkdir(parents=True)
    env = yaml.safe_load(BASE_ENV_CONFIG.read_text())
    env["motion_file"] = reference["file"]
    # The reference is non-looping, so episodes end with the clip.
    env["episode_length"] = reference["duration_s"]
    paths = {name: config_dir / f"{name}.yaml" for name in ("env", "env_play", "agent", "engine")}
    paths["env"].write_text(yaml.safe_dump(env, sort_keys=False))
    # Playback starts at the beginning of the clip instead of a random time.
    paths["env_play"].write_text(yaml.safe_dump({**env, "rand_reset": False}, sort_keys=False))
    shutil.copy(BASE_AGENT_CONFIG, paths["agent"])
    shutil.copy(ENGINE_CONFIG, paths["engine"])
    return paths


def read_final_log_row(log_file: Path) -> dict:
    """Return the last row of MimicKit's txt log (header line followed by value rows)."""
    if not log_file.exists():
        return {}
    tokens = log_file.read_text().split()
    header = []
    for token in tokens:
        try:
            float(token)
            break
        except ValueError:
            header.append(token)
    values = tokens[len(header):]
    if not header or len(values) < len(header):
        return {}
    last = values[(len(values) // len(header) - 1) * len(header):][:len(header)]
    return {key: float(value) for key, value in zip(header, last)}


def new_run_dir(out_root: Path, name: str) -> Path:
    run_dir = out_root / name
    suffix = 1
    while run_dir.exists():
        run_dir = out_root / f"{name}_{suffix}"
        suffix += 1
    run_dir.mkdir(parents=True)
    return run_dir


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("text", help="자연어 동작 명령")
    cli.add_argument("--num-envs", type=int, default=DEFAULT_NUM_ENVS,
                     help=f"병렬 시뮬레이션 수 (기본 {DEFAULT_NUM_ENVS})")
    cli.add_argument("--iters", type=int, default=TRAIN_ITERS, help=f"학습 반복 횟수 (기본 {TRAIN_ITERS})")
    cli.add_argument("--out-root", type=Path, default=OUTPUT_ROOT, help="결과 폴더를 만들 위치 (기본 outputs/)")
    cli.add_argument("--run-name", help="결과 폴더 이름 (기본 <시각>_<동작>)")
    args = cli.parse_args()

    parsed = parse_command(args.text)
    print("파싱 결과:", json.dumps(parsed, ensure_ascii=False), flush=True)

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = new_run_dir(args.out_root.resolve(), args.run_name or f"{stamp}_{parsed['action']}")
    reference = build_reference(parsed, run_dir / "reference.pkl")
    configs = write_configs(run_dir / "config", reference)
    print(f"레퍼런스: {Path(reference['clip']).name}, 회전 {reference['yaw_deg']:.0f}°, "
          f"재생 속도 {reference['playback_rate']:.2f}배, 길이 {reference['duration_s']:.2f}초", flush=True)

    import yaml

    steps_per_iter = yaml.safe_load(configs["agent"].read_text())["steps_per_iter"]
    max_samples = args.iters * args.num_envs * steps_per_iter
    train_dir = run_dir / "train"
    mimickit_args = [
        "--mode", "train", "--num_envs", args.num_envs, "--devices", "cuda:0",
        "--engine_config", configs["engine"], "--env_config", configs["env"],
        "--agent_config", configs["agent"], "--visualize", "false", "--video", "false",
        "--rand_seed", RAND_SEED, "--logger", "txt", "--max_samples", max_samples,
        "--out_dir", train_dir,
    ]
    summary = {
        "command": args.text,
        "parsed": parsed,
        "reference": reference,
        "training": {
            "iterations": args.iters,
            "num_envs": args.num_envs,
            "max_samples": max_samples,
            "mimickit_args": [str(arg) for arg in mimickit_args],
            "started": datetime.datetime.now().isoformat(timespec="seconds"),
            "status": "running",
        },
    }
    summary_file = run_dir / "summary.json"
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"학습 시작: {args.iters}회, 환경 {args.num_envs}개 -> {run_dir}", flush=True)

    try:
        returncode = run_in_isaaclab(mimickit_args, run_dir / "train_console.log")
        status = "completed" if returncode == 0 else f"failed (exit {returncode})"
    except KeyboardInterrupt:
        returncode, status = 130, "interrupted"

    summary["training"].update({
        "status": status,
        "finished": datetime.datetime.now().isoformat(timespec="seconds"),
        "model_file": str(train_dir / "model.pt") if (train_dir / "model.pt").exists() else None,
        "final_log": read_final_log_row(train_dir / "log.txt"),
    })
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"학습 {status}: {run_dir}", flush=True)
    if returncode == 0:
        print(f"재생: ./play_motion.py {os.path.relpath(run_dir, Path.cwd())}", flush=True)
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
