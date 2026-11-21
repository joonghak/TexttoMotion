#!/home/jong/isaaclab/.venv/bin/python
"""Train one trial variant outside the fixed sets of run_style_walk.py.

    ./experiments/style_walk/trials/trial_driver.py <exp_dir> <key> <term=scale,...> [iters]

Example: speed x1.4, 1000 iterations:
    ./experiments/style_walk/trials/trial_driver.py experiments/style_walk/trials/speed2 faster speed=1.4 1000
Compare with other runs by linking them into the same folder and passing --variants to
quality_eval.py and film.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "style_walk"))
import run_style_walk as rs

exp_dir, key = Path(sys.argv[1]).resolve(), sys.argv[2]
scales = {item.split("=")[0]: float(item.split("=")[1]) for item in sys.argv[3].split(",") if item}
iters = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
print(f"trial {key}: scales {scales}, iters {iters}", flush=True)
print(f"trial {key}:", rs.run_variant(exp_dir, key, key, scales, iters, 1024), flush=True)
