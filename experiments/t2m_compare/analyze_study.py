#!/home/jong/isaaclab/.venv/bin/python
"""Results of the blind human study: how often the raters chose each method, per question.

Usage on this computer (after the answers are collected):
    ./experiments/t2m_compare/analyze_study.py <answers.csv> [more.csv ...] [--stimuli experiments/t2m_compare/study/stimuli.json]

Each csv (one per rater from the survey page of make_study_page.py, or one for all) has one row per answer and the
header rater,key,question,choice (position is ignored; seconds, the time on the command's page, gives the study time):
    rater     any id of the rater
    key       the command's key in study/stimuli.json (e.g. set7_N1)
    question  "match" (the video that fits the command best) or "natural" (the most natural video)
    choice    the letter the rater chose, A to D
The letters are turned into methods with each command's answer_key (make_study_films.py). Writes <answers>_results.md
next to a single csv, or study_results.md next to the first of several: per question the share of the choices per
method with a 95 % Wilson interval, a one-sided binomial test of ours against chance (1/4), the method chosen most
per command, and the agreement of the raters (the share of rater pairs that chose the same method, and Fleiss'
kappa, on the commands every rater answered).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

from scipy.stats import binomtest

HERE = Path(__file__).resolve().parent
METHODS = ("ours", "momask", "t2mgpt", "mdm")
NAMES = {"ours": "우리", "momask": "MoMask", "t2mgpt": "T2M-GPT", "mdm": "MDM"}
QUESTIONS = {"match": "명령과 가장 잘 맞는 영상", "natural": "가장 자연스러운 영상"}


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    """95 % Wilson interval of a share k/n."""
    if n == 0:
        return float("nan"), float("nan")
    p, d = k / n, 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def fleiss_kappa(table: list[list[int]]) -> tuple[float, float]:
    """(Fleiss' kappa, share of rater pairs that agree) of items x categories counts; every item has the same number
    of raters (at least 2). Kappa is low when one category takes most answers even if the raters agree, so the plain
    agreement is reported next to it."""
    if not table or sum(table[0]) < 2:
        return float("nan"), float("nan")
    items, raters = len(table), sum(table[0])
    share = [sum(row[j] for row in table) / (items * raters) for j in range(len(table[0]))]
    agree = sum((sum(c * c for c in row) - raters) / (raters * (raters - 1)) for row in table) / items
    chance = sum(p * p for p in share)
    return ((agree - chance) / (1 - chance) if chance < 1 else float("nan")), agree


def read_answers(path: Path, stimuli: dict) -> list[dict]:
    rows, seen = [], set()
    with path.open(newline="", encoding="utf-8-sig") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            row = {k.strip(): (v or "").strip() for k, v in row.items()}
            key, question, letter = row.get("key", ""), row.get("question", ""), row.get("choice", "").upper()
            if key not in stimuli:
                raise ValueError(f"{path}:{line}: key {key!r} is not in the stimuli")
            if question not in QUESTIONS:
                raise ValueError(f"{path}:{line}: question {question!r} must be one of {', '.join(QUESTIONS)}")
            if letter not in stimuli[key]["answer_key"]:
                raise ValueError(f"{path}:{line}: choice {letter!r} must be one of A to D")
            if (row["rater"], key, question) in seen:
                raise ValueError(f"{path}:{line}: rater {row['rater']!r} answered {key} {question} twice")
            seen.add((row["rater"], key, question))
            rows.append({"rater": row["rater"], "key": key, "question": question,
                         "method": stimuli[key]["answer_key"][letter],
                         "seconds": float(row["seconds"]) if row.get("seconds") else None})
    return rows


def report(rows: list[dict], stimuli: dict) -> list[str]:
    raters = sorted({r["rater"] for r in rows})
    lines = ["# 사람 평가 결과", "",
             f"평가자 {len(raters)}명, 명령 {len({r['key'] for r in rows})}개, 답 {len(rows)}개. "
             "선택 비율의 괄호는 95% Wilson 구간이고, p는 우리가 우연(1/4)보다 많이 뽑혔는지 본 한쪽 이항 검정이다.", ""]
    per = {}  # rater -> {key: seconds on that command's page}
    for r in rows:
        if r.get("seconds") is not None:
            per.setdefault(r["rater"], {})[r["key"]] = r["seconds"]
    if per:
        totals = sorted(sum(v.values()) / 60 for v in per.values())
        half = len(totals) // 2
        middle = totals[half] if len(totals) % 2 else (totals[half - 1] + totals[half]) / 2
        lines += [f"평가 시간(문항 화면에 머문 시간의 합, {len(totals)}명): 중앙값 {middle:.1f}분, "
                  f"가장 짧은 평가자 {totals[0]:.1f}분, 가장 긴 평가자 {totals[-1]:.1f}분.", ""]
    for question, title in QUESTIONS.items():
        answers = [r for r in rows if r["question"] == question]
        if not answers:
            continue
        counts, n = Counter(r["method"] for r in answers), len(answers)
        lines += [f"## {title}", "", "| 방법 | 선택 수 | 선택 비율 |", "| --- | --- | --- |"]
        for m in METHODS:
            lo, hi = wilson(counts[m], n)
            lines.append(f"| {NAMES[m]} | {counts[m]}/{n} | {counts[m] / n:.2f} ({lo:.2f}~{hi:.2f}) |")
        p = binomtest(counts["ours"], n, 0.25, alternative="greater").pvalue
        per_key = {}
        for r in answers:
            per_key.setdefault(r["key"], Counter())[r["method"]] += 1
        full = [c for c in per_key.values() if sum(c.values()) == len(raters)]
        kappa, agree = fleiss_kappa([[c[m] for m in METHODS] for c in full])
        lines += ["", f"우리가 뽑힌 비율의 이항 검정 p = {p:.2g}. 모든 평가자가 답한 명령 {len(full)}개에서 평가자 두 사람이 "
                      f"같은 방법을 고른 비율은 {agree:.2f}, Fleiss' kappa는 {kappa:.2f}이다.", "",
                  "| 명령 | 문장 | " + " | ".join(NAMES[m] for m in METHODS) + " | 가장 많이 뽑힌 방법 |",
                  "| --- | --- | " + " | ".join("---" for _ in METHODS) + " | --- |"]
        for key in stimuli:
            if key not in per_key:
                continue
            c = per_key[key]
            top = max(c.values())
            lines.append(f"| {key} | {stimuli[key]['text']} | " + " | ".join(str(c[m]) for m in METHODS)
                         + " | " + ", ".join(NAMES[m] for m in METHODS if c[m] == top) + " |")
        lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("answers", type=Path, nargs="+")
    parser.add_argument("--stimuli", type=Path, default=HERE / "study" / "stimuli.json")
    args = parser.parse_args()
    stimuli = {s["key"]: s for s in json.loads(args.stimuli.read_text())}
    rows, seen = [], set()
    try:
        for path in args.answers:
            for row in read_answers(path, stimuli):
                if (row["rater"], row["key"], row["question"]) in seen:
                    raise ValueError(f"{path}: rater {row['rater']!r} answered {row['key']} {row['question']} in two files")
                seen.add((row["rater"], row["key"], row["question"]))
                rows.append(row)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    lines = report(rows, stimuli)
    first = args.answers[0]
    out = first.with_name(first.stem + "_results.md") if len(args.answers) == 1 else first.with_name("study_results.md")
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
