#!/home/jong/isaaclab/.venv/bin/python
"""Training-free style metric of several LLM runs on one test set, per command and in total (no simulation).

Usage on this computer:
    ./experiments/style_eval/compare_metric.py experiments/style_llm/<run> [<run> ...] [--out x.md]

Reads <run>/style_metric.json (score_generation.py) and results.json of every run. Per command: similarity and rank
of the run's answer against the command's 100STYLE target; a rejected answer or one off the walk counts as no
change (similarity 0, rank 99). Totals: mean similarity, commands ranked first, in the top 5, median rank.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def label(run: Path) -> str:
    summary = json.loads((run / "results.json").read_text())
    model = summary["model"].split("/")[-1].replace("Qwen3-4B-Thinking-2507", "Qwen3-4B")
    effort = summary.get("reasoning_effort")
    return f"{model} {summary['prompt']}" + (f" ({effort})" if effort and effort != "medium" else "")


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("runs", nargs="+", type=Path)
    cli.add_argument("--out", type=Path)
    args = cli.parse_args()
    runs = [run.resolve() for run in args.runs]
    names = [label(run) for run in runs]
    tables = []
    for run in runs:
        metric = json.loads((run / "style_metric.json").read_text())
        tables.append({row["id"]: row for row in metric["results"]})
    commands = json.loads((runs[0] / "results.json").read_text())["results"]
    lines = ["| ID | 명령 | 목표 | " + " | ".join(names) + " |", "| --- | --- | --- | " + " | ".join("---" for _ in names) + " |"]
    sims = [[] for _ in runs]
    ranks = [[] for _ in runs]
    for command in commands:
        if not command.get("target"):
            continue
        cells = []
        for i, table in enumerate(tables):
            row = table.get(command["id"])
            if row is None or row.get("similarity") is None:
                sims[i].append(0.0)
                ranks[i].append(99)
                cells.append("거절/다른 동작")
            else:
                sims[i].append(row["similarity"])
                ranks[i].append(row["rank"])
                cells.append(f"{row['similarity']:.2f} ({row['rank']})")
        lines.append(f"| {command['id']} | {command['text']} | {command['target']} | " + " | ".join(cells) + " |")
    lines.append("| | 유사도 평균 | | " + " | ".join(f"{np.mean(s):.2f}" for s in sims) + " |")
    lines.append("| | 1위 | | " + " | ".join(str(sum(r == 1 for r in rk)) for rk in ranks) + " |")
    lines.append("| | 5위 이내 | | " + " | ".join(str(sum(r <= 5 for r in rk)) for rk in ranks) + " |")
    lines.append("| | 순위 중앙값 | | " + " | ".join(f"{np.median(rk):g}" for rk in ranks) + " |")
    text = "\n".join(lines) + "\n"
    if args.out:
        args.out.write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
