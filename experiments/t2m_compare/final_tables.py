#!/home/jong/isaaclab/.venv/bin/python
"""The tables of the final evaluation: our final policies and the three text-to-motion models on sets 7 to 10.

Usage on this computer (after experiments/style_walk/final_runs.sh and the baselines' measurements):
    ./experiments/t2m_compare/final_tables.py

Reads, for ours, the final experiment folders experiments/style_walk/*_f<set>_set<set>_final (evaluate.log of
evaluate_policies.py for the 100STYLE metric, out/ours_set8_<exp>_measures.json, side_check.json, chain_check.json and
the rollouts for physics), and for the baselines out/<method>_style_metric.json, <method>_measures.json,
<method>_side_check.json and <method>_chain_check.json. Writes out/final_tables.md. A table row is left out when a
method has no result for it yet.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "style_eval"))

import measure as ms  # noqa: E402

BASELINES = {"momask": "MoMask", "t2mgpt": "T2M-GPT", "mdm": "MDM"}
PHYSICS = ("penetration_cm", "floating_cm", "slide_cm", "skate")


def final_exp(set_name: str) -> Path | None:
    found = sorted(glob.glob(str(ROOT / "experiments" / "style_walk" / f"*_f{set_name}_set{set_name}_final")))
    return Path(found[-1]) if found else None


def ours_style(exp: Path, with_rank: bool = False) -> dict:
    """{command id: similarity} of our trained policies (evaluate_policies.py report next to the set file), or
    {command id: (similarity, rank of the target among the 99 styles)} with with_rank."""
    report = ROOT / "experiments" / "style_eval" / "sets" / f"final_set{exp.name.split('_set')[-1].split('_')[0]}_report.json"
    if not report.exists():
        return {}
    rows = json.loads(report.read_text())
    rows = rows.get("results", rows) if isinstance(rows, dict) else rows
    return {r["label"].split("_", 1)[1]: ((r.get("similarity"), r.get("rank")) if with_rank else r.get("similarity"))
            for r in rows if r.get("similarity") is not None}


def t2m_ranks(method: str, set_name: str) -> dict:
    """{command id: [rank of the target per output, None when the output could not be measured]}."""
    path = OUT / f"{method}_style.json"
    if not path.exists():
        return {}
    by_id = {}
    for key, r in json.loads(path.read_text()).items():
        if key.startswith(f"set{set_name}_"):
            by_id.setdefault(key.split("_")[1], []).append(r.get("rank"))
    return by_id


def style_groups(set_name: str, ours: dict, base: dict, ranks: dict) -> list:
    """Lines of the per-group table of a set's 100STYLE similarity and the share of targets in the top 5 of 99."""
    spec = json.loads((ROOT / "experiments" / "style_llm" / f"test_commands_{set_name}.json").read_text())
    group_of = {c["id"]: c["group"] for c in spec["commands"]}
    lines = [f"표: {set_name}세트 명령 종류별 100STYLE 유사도 (비교 모델은 잴 수 있는 출력의 평균)", "",
             "| 종류 | 명령 수 | 우리 | " + " | ".join(BASELINES.values()) + " |",
             "| --- | --- | --- | " + " | ".join("---" for _ in BASELINES) + " |"]

    def cell(values):
        values = [v for v in values if v is not None]
        return f"{np.mean(values):.2f}" if values else "-"

    for g, title in spec["groups"].items():
        ids = [cid for cid, gg in group_of.items() if gg == g]
        lines.append(f"| {title} | {len(ids)} | {cell([ours[c][0] for c in ids if c in ours])} | "
                     + " | ".join(cell([base[m][c][0] for c in ids if c in base[m]]) for m in BASELINES) + " |")
    top = [f"우리 {sum(1 for s, r in ours.values() if r is not None and r <= 5)}/{len(ours)}"] if ours else []
    for m, name in BASELINES.items():
        all_ranks = [r for rs in ranks[m].values() for r in rs]
        if all_ranks:
            top.append(f"{name} {sum(1 for r in all_ranks if r is not None and r <= 5)}/{len(all_ranks)}")
    return lines + ["", "목표 스타일이 99개 가운데 5위 안에 든 경우 (우리는 명령마다 정책 하나, 비교 모델은 출력마다): "
                    + ", ".join(top), ""]


def t2m_style(method: str, set_name: str) -> dict:
    """{command id: (mean similarity of the measured outputs, mean with unmeasured outputs as 0)} on a set
    (style_metric_t2m.py)."""
    path = OUT / f"{method}_style.json"
    if not path.exists():
        return {}
    by_id = {}
    for key, r in json.loads(path.read_text()).items():
        if key.startswith(f"set{set_name}_"):
            by_id.setdefault(key.split("_")[1], []).append(r["similarity"])
    return {cid: (float(np.mean([v for v in vals if v is not None])) if any(v is not None for v in vals) else None,
                  float(np.mean([v if v is not None else 0.0 for v in vals]))) for cid, vals in by_id.items()}


def policy_rows(exp: Path) -> list:
    """Physics of each policy of a final set: the mean over its four characters, which start alike and move
    alike (they differ by at most about 0.1 cm here), so that a policy counts once."""
    rows = []
    for f in sorted(glob.glob(str(ROOT / "experiments" / "style_eval" / "rollouts" / f"{exp.name}__*.npz"))):
        found = [r for r in ms.measure_ours(Path(f)) if "penetration_cm" in r]
        if found:
            rows.append({m: float(np.nanmean([r[m] for r in found])) for m in PHYSICS})
    return rows


def physics_stats(rows: list) -> dict:
    """Means over motions, the slide as the median over them."""
    return {m: (float(np.nanmedian([r[m] for r in rows])) if m == "slide_cm" else float(np.nanmean([r[m] for r in rows])))
            for m in PHYSICS} | {"n": len(rows)}


def t2m_rows(method: str, sets: tuple) -> list:
    """Outputs of a baseline on the given sets; set 8's plain walk (Q0, "A person walks forward.") is the base
    of the comparison, not one of the commands, and is left out."""
    path = OUT / f"{method}_measures.json"
    if not path.exists():
        return []
    rows = json.loads(path.read_text())["rows"]
    return [r for k, r in rows.items() if k.split("_")[0] in tuple(f"set{x}" for x in sets)
            and not k.startswith("set8_Q0") and "penetration_cm" in r]


def main() -> int:
    lines = ["# 최종 평가 표 (우리 최종 정책과 공개 T2M 모델 세 개)", ""]
    # 7세트: 100STYLE
    exp7 = final_exp("7")
    ours = ours_style(exp7) if exp7 else {}
    base = {m: t2m_style(m, "7") for m in BASELINES}
    if ours or any(base.values()):
        lines += ["## 7세트 (평가용 스타일): 100STYLE 유사도", "",
                  "비교 모델은 명령마다 출력 3개의 평균이다. 곧게 걷지 못해 잴 수 없는 출력은 빼고 낸 값과, 0으로 넣은 값을 함께 적었다.", "",
                  "| 방법 | 유사도 평균 | 잴 수 없는 출력을 0으로 | 명령 수 |", "| --- | --- | --- | --- |"]
        if ours:
            lines.append(f"| 우리 ({exp7.name}) | {np.mean(list(ours.values())):.2f} | - | {len(ours)} |")
        for m, name in BASELINES.items():
            vals = base[m]
            if vals:
                measured = [a for a, _ in vals.values() if a is not None]
                lines.append(f"| {name} | {np.mean(measured):.2f} | {np.mean([b for _, b in vals.values()]):.2f} | {len(vals)} |")
        lines.append("")
        lines += style_groups("7", ours_style(exp7, with_rank=True) if exp7 else {}, base,
                              {m: t2m_ranks(m, "7") for m in BASELINES})
    # 8세트: numbers (compare_set8.py writes the full table)
    exp8 = final_exp("8")
    if exp8 and (OUT / f"set8_compare_{exp8.name}.md").exists():
        tail = (OUT / f"set8_compare_{exp8.name}.md").read_text().strip().split("\n")[-2:]
        lines += ["## 8세트 (수치를 말한 명령)", "", f"표 전체: `out/set8_compare_{exp8.name}.md`", ""] + tail + [""]
    # 9세트: one-sided checks
    exp9 = final_exp("9")
    rows9 = []
    if exp9 and (exp9 / "side_check.json").exists():
        variants = json.loads((exp9 / "side_check.json").read_text())["variants"]
        passed = sum(v.get("passed", 0) for v in variants.values() if "values" in v)
        total = sum(len(v["values"]) for v in variants.values() if "values" in v)
        rows9.append(f"| 우리 ({exp9.name}) | {passed}/{total} (캐릭터 4개씩) |")
    for m, name in BASELINES.items():
        path = OUT / f"{m}_side_check.json"
        if path.exists():
            data = json.loads(path.read_text())
            rows9.append(f"| {name} | {sum(v['passed'] for v in data.values())}/{sum(len(v['values']) for v in data.values())} (출력 3개씩) |")
    if rows9:
        lines += ["## 9세트 (한쪽 동작): 확인 식 통과", "", "| 방법 | 통과 |", "| --- | --- |"] + rows9 + [""]
    # 10세트: chain order
    exp10 = final_exp("10")
    rows10 = []
    if exp10 and (exp10 / "chain_check.json").exists():
        data = json.loads((exp10 / "chain_check.json").read_text())
        rows10.append(f"| 우리 ({exp10.name}) | {sum(sum(v['pass']) for v in data.values())}/{sum(len(v['pass']) for v in data.values())} |")
    for m, name in BASELINES.items():
        path = OUT / f"{m}_chain_check.json"
        if path.exists():
            data = json.loads(path.read_text())
            rows10.append(f"| {name} | {sum(sum(v['pass']) for v in data.values())}/{sum(len(v['pass']) for v in data.values())} |")
    if rows10:
        lines += ["## 10세트 (동작 이어붙이기): 요청한 순서로 모든 동작이 나온 비율", "", "| 방법 | 통과 |", "| --- | --- |"] + rows10 + [""]
    # physics: ours one row per policy, the baselines one row per output (set 8's plain walk left out)
    rows_p = []
    ours = {x: (policy_rows(final_exp(x)) if final_exp(x) else []) for x in ("7", "8", "9", "10")}
    groups = [(f"우리, {x}세트", ours[x]) for x in ("7", "8", "9", "10")]
    groups += [("우리, 7~9세트 (걷기)", ours["7"] + ours["8"] + ours["9"]), ("우리, 7~10세트", sum(ours.values(), []))]
    for m, name in BASELINES.items():
        groups += [(f"{name}, 7~9세트 (걷기)", t2m_rows(m, ("7", "8", "9"))), (f"{name}, 7~10세트", t2m_rows(m, ("7", "8", "9", "10"))),
                   (f"{name}, 8세트", t2m_rows(m, ("8",)))]
    for name, group in groups:
        if group:
            st = physics_stats(group)
            rows_p.append(f"| {name} | {st['n']} | {st['penetration_cm']:.2f} | {st['floating_cm']:.2f} | "
                          f"{st['slide_cm']:.2f} | {st['skate']:.3f} |")
    if rows_p:
        lines += ["## 물리 지표", "", "우리는 정책 수(정책마다 캐릭터 4개의 평균), 비교 모델은 출력 수이다.", "",
                  "| 방법과 묶음 | 수 | 땅 뚫기 (cm) | 떠 있음 (cm) | 디딘 발 미끄러짐 (cm, 중앙값) | 빠른 미끄러짐 비율 |",
                  "| --- | --- | --- | --- | --- | --- |"] + rows_p + [""]
    (OUT / "final_tables.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
