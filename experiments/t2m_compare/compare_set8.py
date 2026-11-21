#!/home/jong/isaaclab/.venv/bin/python
"""Set 8 (numbers stated in the command) side by side: our policies and the three text-to-motion models.

Usage on this computer (after summarize.py for every method and for ours):
    ./experiments/t2m_compare/compare_set8.py [our experiment name]   # default: the luna v10 run of 11-12

Reads out/<method>_measures.json and out/ours_set8_measures.json and writes out/set8_compare.md: per command the
stated value, each method's mean measured value and its mean absolute error; the lean commands also read above the
waist (upper_lean). Lower error is better; the best method of each row is marked.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import summarize as sm  # noqa: E402

METHODS = {"ours": "우리 (luna v10, 학습한 정책)", "momask": "MoMask", "t2mgpt": "T2M-GPT", "mdm": "MDM"}


def upper_values(data: dict, method: str, cid: str, command: dict) -> list:
    plain = data["plain"]
    if method == "ours":
        rows = data["rows"].get(cid) or []
    else:
        rows = [r for key, r in data["rows"].items() if key.startswith(f"set8_{cid}_r")]
    return [sm.stated_value(r, plain, command["measure"], sm.UPPER) if "error" not in r else float("nan") for r in rows]


def main() -> int:
    commands = [c for c in json.loads(sm.SET8.read_text())["commands"] if c["measure"] != "plain"]
    ours = sys.argv[1] if len(sys.argv) > 1 else "20261112_154003_luna_v10_set8_trained"
    data = {m: json.loads((HERE / "out" / (f"{m}_measures.json" if m != "ours" else f"ours_set8_{ours}_measures.json")).read_text())
            for m in METHODS}
    METHODS["ours"] = f"우리 ({ours})"
    head = "| ID | 명령 | 말한 값 | " + " | ".join(METHODS.values()) + " |"
    lines = ["# 8세트: 명령에 말한 값과 잰 값 (평균, 괄호는 평균 절대 오차)", "",
             "각도는 각 방법의 기본 걷기와의 차이, 박자와 속도는 절대값, 보폭은 기본 걷기에 대한 배율이다. 행마다 오차가 가장 "
             "작은 방법을 굵게 표시하였다. 상체 기울기는 골반에서 목까지의 선과, 허리(우리 몸통 관절, HumanML3D spine2)에서 "
             "목까지의 선으로 두 번 잰다.", "", head, "|" + " --- |" * (3 + len(METHODS))]
    wins = {m: 0 for m in METHODS}
    errors = {m: [] for m in METHODS}

    def row(label: str, command: dict, values: dict, count: bool = True) -> None:
        cells, errs = [], {}
        for m in METHODS:
            vals = [v for v in values[m] if np.isfinite(v)]
            if not vals:
                cells.append("-")
                continue
            errs[m] = float(np.mean([abs(v - command["value"]) for v in vals]))
            cells.append(f"{np.mean(vals):.2f} ({errs[m]:.2f})")
        best = min(errs, key=errs.get) if errs else None
        if best and count:
            wins[best] += 1
            for m, e in errs.items():
                errors[m].append(e / max(abs(command["value"]), 1e-6))
        if best:
            cells[list(METHODS).index(best)] = f"**{cells[list(METHODS).index(best)]}**"
        lines.append(f"| {command['id']} | {label} | {command['value']} | " + " | ".join(cells) + " |")

    for c in commands:
        row(c["text"], c, {m: data[m]["set8"].get(c["id"], {}).get("measured", []) for m in METHODS})
        if c["measure"] in sm.UPPER:
            row(c["text"] + " (허리 위)", c, {m: upper_values(data[m], m, c["id"], c) for m in METHODS}, count=False)
    lines += ["", "아래 두 합계는 명령마다 한 번씩(상체 기울기는 골반에서 목까지의 값으로) 센다.", "",
              "오차가 가장 작은 행의 수: " + ", ".join(f"{METHODS[m]} {wins[m]}" for m in METHODS),
              "말한 값에 대한 상대 오차의 중앙값: " + ", ".join(f"{METHODS[m]} {np.median(errors[m]) * 100:.0f}%"
                                                     for m in METHODS if errors[m])]
    out = HERE / "out" / f"set8_compare_{ours}.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
