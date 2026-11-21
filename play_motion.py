#!/home/jong/isaaclab/.venv/bin/python
"""Replay a policy trained by train_from_text.py in the Isaac Lab viewer.

Usage on this computer:
    ./play_motion.py                                  # most recent run in outputs/
    ./play_motion.py outputs/20260922_153000_spinkick  # a specific run folder
    ./play_motion.py --list                           # list trained runs
    ./play_motion.py --no-ref <결과 폴더>              # hide the green reference character

The policy starts at the beginning of its reference clip; each episode ends with
the clip and restarts. Close the viewer window or press Ctrl+C to stop.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from train_from_text import OUTPUT_ROOT, run_in_isaaclab

# Fallbacks for this machine's desktop session; only used when the shell has none.
DEFAULT_DISPLAY = ":1"
DEFAULT_XAUTHORITY = "/run/user/1000/gdm/Xauthority"


def trained_runs() -> list:
    """Run folders with a trained model, oldest first."""
    if not OUTPUT_ROOT.exists():
        return []
    return sorted(path for path in OUTPUT_ROOT.iterdir() if (path / "train" / "model.pt").exists())


def describe(run_dir: Path) -> str:
    summary_file = run_dir / "summary.json"
    if not summary_file.exists():
        return run_dir.name
    summary = json.loads(summary_file.read_text())
    status = summary.get("training", {}).get("status", "?")
    return f"{run_dir.name}  [{status}]  {summary.get('command', '')}"


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("run_dir", nargs="?", help="재생할 결과 폴더 (생략하면 가장 최근 결과)")
    cli.add_argument("--list", action="store_true", help="학습된 결과 목록 출력")
    cli.add_argument("--num-envs", type=int, default=1, help="동시에 재생할 캐릭터 수 (기본 1)")
    cli.add_argument("--no-ref", action="store_true", help="이번 재생에서만 초록 레퍼런스 캐릭터 숨기기")
    args = cli.parse_args()

    runs = trained_runs()
    if args.list:
        for run_dir in runs:
            print(describe(run_dir))
        return 0
    if args.run_dir is not None:
        run_dir = Path(args.run_dir).expanduser()
        run_dir = run_dir if run_dir.is_absolute() else (Path.cwd() / run_dir)
    elif runs:
        run_dir = runs[-1]
    else:
        print(f"학습된 결과가 없습니다: {OUTPUT_ROOT}", file=sys.stderr)
        return 1
    return play(run_dir, args.num_envs, show_ref=not args.no_ref)


def play(run_dir: Path, num_envs: int = 1, show_ref: bool = True) -> int:
    """Open the viewer for one run folder; returns when the viewer closes."""
    config_dir, model_file = run_dir / "config", run_dir / "train" / "model.pt"
    required = [config_dir / "env_play.yaml", config_dir / "agent.yaml", config_dir / "engine.yaml", model_file]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("필요한 파일이 없습니다:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1

    print("재생:", describe(run_dir), flush=True)
    os.environ.setdefault("DISPLAY", DEFAULT_DISPLAY)
    os.environ.setdefault("XAUTHORITY", DEFAULT_XAUTHORITY)
    env_config, temp_config = config_dir / "env_play.yaml", None
    if not show_ref:
        import yaml

        # A throwaway copy, so the saved run folder keeps showing the reference by default.
        config = yaml.safe_load(env_config.read_text())
        config["visualize_ref_char"] = False
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump(config, f, sort_keys=False)
        env_config = temp_config = Path(f.name)
    try:
        return run_in_isaaclab([
            "--mode", "test", "--num_envs", num_envs, "--devices", "cuda:0",
            "--engine_config", config_dir / "engine.yaml", "--env_config", env_config,
            "--agent_config", config_dir / "agent.yaml", "--visualize", "true",
            "--model_file", model_file,
        ])
    except KeyboardInterrupt:
        return 130
    finally:
        if temp_config is not None:
            temp_config.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
