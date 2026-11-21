#!/home/jong/isaaclab/.venv/bin/python
"""100STYLE similarity of a text-to-motion model's outputs, the metric our policies get (experiments/style_eval).

Usage on this computer:
    ./experiments/t2m_compare/style_metric_t2m.py momask t2mgpt mdm

For every output out/<method>/set<N>_<id>_r<k>.npy of a command with a 100STYLE target (sets 6, 7 and 9), the gait
features of its steady straight walking are compared with the same method's plain walk (out/<method>_plain, the median
of each feature over its outputs), as our policies are compared with our plain walk. An output without enough steady
straight walking cannot be measured; it is kept as null and reported both ways (left out, and counted as 0).
Writes out/<method>_style.json ({key: {"target", "similarity", "rank"}}) and prints the mean per set.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "style_eval"))

import gait_features as gf  # noqa: E402
import measure as ms  # noqa: E402
import style_metric as sm  # noqa: E402

SETS = {n: ROOT / "experiments" / "style_llm" / f"test_commands_{n}.json" for n in ("6", "7", "9")}


def feats(path: str):
    joints = np.load(path)
    joints = joints[0] if joints.ndim == 4 else joints
    try:
        return gf.features(ms.hml_points(joints), ms.HML_FPS, min_frames=int(2 * ms.HML_FPS))
    except ValueError:
        return None


def main() -> int:
    ref = sm.Reference()
    targets = {f"set{n}_{c['id']}": c.get("target") for n, f in SETS.items() for c in json.loads(f.read_text())["commands"]}
    for method in sys.argv[1:]:
        plain_rows = [x for x in (feats(f) for f in sorted(glob.glob(str(HERE / "out" / f"{method}_plain" / "*.npy")))) if x]
        plain = {name: float(np.median([r[name] for r in plain_rows])) for name in gf.FEATURES}
        out = {}
        for f in sorted(glob.glob(str(HERE / "out" / method / "set*_r*.npy"))):
            key = Path(f).stem
            command = key.rsplit("_r", 1)[0]
            if not targets.get(command):
                continue
            f_out = feats(f)
            if f_out is None:
                out[key] = {"target": targets[command], "similarity": None, "rank": None}
                continue
            result = ref.evaluate(gf.style_delta(f_out, plain), target=targets[command], top=3)
            out[key] = {"target": targets[command], "similarity": result["similarity"], "rank": result["rank"]}
        (HERE / "out" / f"{method}_style.json").write_text(json.dumps(out, indent=1))
        for n in SETS:
            rows = [v for k, v in out.items() if k.startswith(f"set{n}_")]
            if not rows:
                continue
            sims = [r["similarity"] for r in rows]
            measured = [s for s in sims if s is not None]
            print(f"{method} set {n}: {len(rows)} outputs, measured {len(measured)}, mean {np.mean(measured):.2f} "
                  f"(unmeasured as 0: {np.mean([s if s is not None else 0.0 for s in sims]):.2f})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
