#!/usr/bin/env python3
"""How many policies this project has trained, for the report: every train/model.pt under experiments/ and outputs/,
counted once per training run, by phase, reference clip and iteration budget, with GPU hours and samples.

Usage on this computer:
    python3 experiments/count_trainings.py

Searched: experiments/, outputs/ and MimicKit/output/ (the spinkick reproduction). One training run = one (weights,
start time) pair: a folder copied from another experiment (a plain walk linked or
copied as "base") has the same weights and the same start time in its summary.json and is counted once. A policy
trained again with the same values gets the same weights (training is deterministic with the fixed seed) but a
different start time, so it is counted as its own run. A run whose log ends before 500 iterations was stopped and is
listed apart; so is the run being trained now. Phases: up to the midterm report (2026-10-26), development after it,
and the final evaluation runs (experiment folders ending in _final). Iterations, samples and GPU hours are read from
the last row of each run's train/log.txt.
"""

from __future__ import annotations

import collections
import datetime
import hashlib
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDTERM = "2026-10-26"
CLIPS = ("chain", "spinkick", "kick", "jump", "run", "walk")


def last_row(log: Path) -> dict:
    """The last row of a MimicKit txt log (column names, then the values of every logged iteration)."""
    tokens = log.read_text(errors="ignore").split()
    names = []
    for t in tokens:
        try:
            float(t)
            break
        except ValueError:
            names.append(t)
    numbers = [v for v in tokens[len(names):] if re.fullmatch(r"[-+0-9.eE]+|nan|inf", v)]
    if not names or len(numbers) < len(names):
        return {}
    return dict(zip(names, (float(x) for x in numbers[-len(names):])))


def clip_of(run: Path, train: Path) -> str:
    for config in (run / "config" / "env.yaml", train / "env_config.yaml"):
        if config.exists():
            m = re.search(r"motion_file:\s*(\S+)", config.read_text())
            if m:
                name = Path(m.group(1)).name
                return next((c for c in CLIPS if c in name), "other")
    return "other"


def main() -> int:
    seen, runs = set(), []
    found = [m for d in ("experiments", "outputs", "MimicKit/output") for m in (ROOT / d).rglob("model.pt")]
    for model in sorted(found):
        train = model.parent
        run = train.parent if train.name == "train" else train
        info = {}
        if (run / "summary.json").exists():
            try:
                info = json.loads((run / "summary.json").read_text()).get("training", {})
            except ValueError:
                pass
        key = (hashlib.md5(model.read_bytes()).hexdigest(), info.get("started"))
        if key in seen:
            continue
        seen.add(key)
        row = last_row(train / "log.txt") if (train / "log.txt").exists() else {}
        started = info.get("started") or datetime.datetime.fromtimestamp(model.stat().st_mtime).isoformat()
        runs.append({"run": str(run.relative_to(ROOT)), "iterations": int(row.get("Iteration", -1)) + 1,
                     "samples": row.get("Samples", 0.0), "hours": row.get("Wall_Time", 0.0), "date": started[:10],
                     "clip": clip_of(run, train),
                     "running": info.get("status") == "running" and (run / "train_console.log").exists()
                     and time.time() - (run / "train_console.log").stat().st_mtime < 600,
                     "phase": ("3 최종 평가 (11-16~)" if run.name != "base" and "_final" in str(run) else
                               "1 중간보고서까지 (~10-26)" if started[:10] <= MIDTERM else "2 중간 이후 개발 (10-27~11-15)")})
    done = [r for r in runs if r["iterations"] >= 500 and not r["running"]]
    lines = ["| 단계 | 학습 수 | GPU 시간 | 샘플 (억) | 참조 클립 | 반복 수 |", "| --- | --- | --- | --- | --- | --- |"]
    for phase in sorted({r["phase"] for r in done}):
        rs = [r for r in done if r["phase"] == phase]
        clips = collections.Counter(r["clip"] for r in rs)
        iters = collections.Counter(r["iterations"] for r in rs)
        lines.append(f"| {phase} | {len(rs)} | {sum(r['hours'] for r in rs):.1f} | {sum(r['samples'] for r in rs) / 1e8:.0f} | "
                     + ", ".join(f"{c} {n}" for c, n in clips.most_common()) + " | "
                     + ", ".join(f"{i}회 {n}" for i, n in sorted(iters.items(), reverse=True)) + " |")
    lines.append(f"| 합계 | {len(done)} | {sum(r['hours'] for r in done):.1f} | {sum(r['samples'] for r in done) / 1e8:.0f} | | |")
    print("\n".join(lines))
    others = [r for r in runs if r not in done]
    if others:
        print("\n세지 않은 것: " + ", ".join(f"{r['run']} ({r['iterations']}회{', 학습 중' if r['running'] else ', 중단'})" for r in others))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
