#!/home/jong/isaaclab/.venv/bin/python
"""Answers of several prompt runs on one test set, side by side, with the set's value checks (no model).

Usage on this computer:
    ./experiments/style_llm/compare_prompts.py experiments/style_llm/<v4 run> experiments/style_llm/<v5 run> [--out x.md]

A check (test_commands_5.json) is a Python expression over the parameters with defaults filled in; a parameter an
older prompt did not know (stance_width for v4) takes its default. A rejected answer to an accept command fails its
check, and a check that is not a Python expression (some of set 4) is shown but not evaluated.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import style_parser as sp  # noqa: E402


def run_check(check: str, params: dict | None):
    """True or False for an evaluable check, None when the check is free text."""
    if params is None:
        return False
    values = {name: params.get(name, default) for name, (_, _, default) in sp.PARAMS.items()}
    values["action"] = params.get("action", "walk")
    try:
        return bool(eval(check, {"__builtins__": {}}, values))
    except (SyntaxError, NameError, TypeError):
        return None


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("runs", nargs="+", type=Path, help="results.json가 있는 생성 결과 폴더 (같은 테스트 세트)")
    cli.add_argument("--out", type=Path, help="표를 쓸 파일 (없으면 화면에 출력)")
    args = cli.parse_args()
    runs = [json.loads((folder / "results.json").read_text()) for folder in args.runs]
    sets = {run["test_set"] for run in runs}
    if len(sets) != 1:
        cli.error("같은 테스트 세트의 결과만 비교한다: " + ", ".join(sorted(sets)))
    commands = json.loads((HERE / sets.pop()).read_text())["commands"]
    labels = [run["prompt"] for run in runs]
    rows = [{row["id"]: row for row in run["results"]} for run in runs]

    header = "| ID | 명령 | 값 기준 | " + " | ".join(f"{label} 답 | {label} 기준" for label in labels) + " |"
    lines = [header, "|" + " --- |" * (3 + 2 * len(labels))]
    totals = [[0, 0, 0] for _ in labels]  # level 1 passed, checks passed, checks evaluated
    for command in commands:
        check = command.get("check")
        cells = []
        for total, by_id in zip(totals, rows):
            row = by_id[command["id"]]
            total[0] += row["level1"] == "pass"
            params = row.get("params")
            if params is not None:
                answer = sp.compact({name: params.get(name, default) for name, (_, _, default) in sp.PARAMS.items()}
                                    | {"action": params["action"]})
                answer += "".join(f" ({note})" for note in row.get("rules", []))
            else:
                answer = f"거절 ({row['rejection']})"
            if row["level1"] != "pass":
                answer += " [1단계 실패]"
            verdict = "-"
            if check and command["expect"] == "accept":
                result = run_check(check, params)
                if result is not None:
                    total[1] += result
                    total[2] += 1
                    verdict = "통과" if result else "실패"
            cells.append(f"{answer} | {verdict}")
        lines.append(f"| {command['id']} | {command['text']} | {check or '-'} | " + " | ".join(cells) + " |")
    summary = []
    for label, t, run, folder in zip(labels, totals, runs, args.runs):
        tokens = [row["tokens"] for row in run["results"]]
        full = sum(n > run["thinking_budget"] for n in tokens)  # the first pass hit the budget (retries add up)
        summary.append(f"{label}: 1단계 통과 {t[0]}/{len(commands)}, 값 기준 통과 {t[1]}/{t[2]}, 생성 "
                       f"{run['elapsed_s'] / 60:.0f}분, 가장 긴 답 {max(tokens)}토큰, 생각 예산을 다 쓴 답 {full}개 "
                       f"(폴더 {folder.name})")
    text = "\n".join(lines) + "\n\n" + "\n".join(f"- {line}" for line in summary) + "\n"
    if args.out:
        args.out.write_text(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
