#!/home/jong/isaaclab/.venv/bin/python
"""How close the style parameters can get to each 100STYLE style, without training (random search on target motions).

Usage on this computer:
    ./experiments/style_eval/expressibility.py [--samples 1500] [--seed 0]

Draws random parameter sets on the walk (each parameter left at its default with probability 0.5, else uniform in
RANGES), plays their style targets (target_features.py) and reports, for every 100STYLE style, the best similarity
any sample reaches and with which values. A style no sample comes close to needs something the parameters cannot
express; the features it changes most say what. Writes expressibility.md and .json here.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "style_llm"))

import gait_features as gf  # noqa: E402
import style_metric as sm  # noqa: E402

# Ranges searched: the parser's ranges, with m_knee down to 0.4 and the shoulders in to -15 (trained 2026-11-05).
RANGES = {"s": (0.3, 1.8), "n": (0.55, 1.45), "c": (0.0, 30.0), "m_arm": (0.0, 1.8), "m_torso": (0.0, 10.0),
          "m_knee": (0.4, 1.5), "m_elbow": (0.0, 1.0), "torso_pitch": (-15.0, 40.0), "head_pitch": (-15.0, 30.0),
          "shoulder_flexion": (0.0, 85.0), "shoulder_abduction": (-15.0, 85.0), "elbow_flexion": (-30.0, 60.0),
          "stance_width": (0.0, 10.0), "toe_out": (-20.0, 30.0)}
# The ranges before 2026-11-05 (prompt v5, commit c79315f): no toe_out, arms swing at least 0.3, knees at least 0.7,
# the shoulders not moved inward. --before compares the base of last week with this week's.
RANGES_BEFORE = {**{k: v for k, v in RANGES.items() if k != "toe_out"},
                 "m_arm": (0.3, 1.8), "m_knee": (0.7, 1.5), "shoulder_abduction": (0.0, 85.0)}
# The ranges added on 2026-11-11 (--wide): arms back, arms turned about their own axis, legs together, toes further in.
RANGES_WIDE = {**RANGES, "shoulder_flexion": (-45.0, 85.0), "shoulder_rotation": (-45.0, 60.0),
               "stance_width": (-8.0, 10.0), "toe_out": (-35.0, 30.0), "bounce": (0.0, 30.0)}


def sample(rng: np.random.Generator, count: int, ranges: dict = RANGES) -> list:
    import style_parser as sp

    sets = [{"key": "_base", "scales": {}, "params": {}}]
    for i in range(count):
        params = {}
        for name, (low, high) in ranges.items():
            if rng.random() < 0.5:
                params[name] = round(float(rng.uniform(low, high)), 2)
        if params.get("shoulder_flexion", 0) > 0 and params.get("shoulder_abduction", 0) > 0:
            params.pop("shoulder_abduction" if rng.random() < 0.5 else "shoulder_flexion")
        full = {name: params.get(name, default) for name, (_, _, default) in sp.PARAMS.items()}
        sp.companion_rules(full)
        sets.append({"key": f"r{i}", "scales": sp.to_scales(full), "params": params})
    return sets


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("--samples", type=int, default=1500)
    cli.add_argument("--seed", type=int, default=0)
    cli.add_argument("--before", action="store_true", help="the ranges before 2026-11-05 (writes *_before files)")
    cli.add_argument("--wide", action="store_true", help="the ranges of 2026-11-11 (writes *_wide files)")
    args = cli.parse_args()
    rng = np.random.default_rng(args.seed)
    suffix = "_before" if args.before else "_wide" if args.wide else ""
    sets = sample(rng, args.samples, RANGES_BEFORE if args.before else RANGES_WIDE if args.wide else RANGES)
    sets_file = HERE / "targets" / f"random{suffix}.json"
    sets_file.parent.mkdir(exist_ok=True)
    sets_file.write_text(json.dumps(sets, ensure_ascii=False))
    proc = subprocess.run([str(HERE / "target_features.py"), str(sets_file)], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    feats_file = sets_file.with_name(sets_file.stem + "_targets.json")
    if proc.returncode != 0 or not feats_file.exists():
        print(proc.stdout[-3000:], file=sys.stderr)
        return 1
    feats = json.loads(feats_file.read_text())
    ref = sm.Reference()
    keys = [s["key"] for s in sets[1:] if "error" not in feats.get(s["key"], {"error": 1})]
    deltas = np.stack([ref.scaled(gf.style_delta(feats[k], feats["_base"])) for k in keys])
    deltas = np.nan_to_num(deltas)
    unit = deltas / (np.linalg.norm(deltas, axis=1, keepdims=True) + 1e-12)
    refs = np.nan_to_num(ref.deltas)
    refs_unit = refs / (np.linalg.norm(refs, axis=1, keepdims=True) + 1e-12)
    sims = refs_unit @ unit.T  # [styles, samples]
    params_of = {s["key"]: s["params"] for s in sets}
    rows = []
    for i, name in enumerate(ref.names):
        best = int(np.argmax(sims[i]))
        order = np.argsort(-np.abs(refs[i]))[:4]
        rows.append({"style": name, "best": round(float(sims[i, best]), 3), "params": params_of[keys[best]],
                     "main_features": [f"{ref.features[j]} {refs[i, j]:+.1f}" for j in order]})
    rows.sort(key=lambda r: -r["best"])
    lines = [f"# 파라미터로 닿을 수 있는 100STYLE 스타일 (무작위 {len(keys)}개, 목표 동작 기준)", "",
             "가장 높은 유사도 순서이다. 주요 특징은 그 스타일이 Neutral에서 가장 크게 바뀐 특징(같은 단위)이다.", "",
             "| 스타일 | 최고 유사도 | 주요 특징 | 그때의 값 |", "| --- | --- | --- | --- |"]
    for r in rows:
        values = ", ".join(f"{k} {v:g}" for k, v in r["params"].items())
        lines.append(f"| {r['style']} | {r['best']:.2f} | {', '.join(r['main_features'])} | {values} |")
    best = np.array([r["best"] for r in rows])
    lines += ["", f"최고 유사도 0.7 이상 {int((best >= 0.7).sum())}종, 0.5~0.7 {int(((best >= 0.5) & (best < 0.7)).sum())}종, "
                  f"0.5 미만 {int((best < 0.5).sum())}종 (99종)"]
    (HERE / f"expressibility{suffix}.md").write_text("\n".join(lines) + "\n")
    (HERE / f"expressibility{suffix}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print("\n".join(lines[-1:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
