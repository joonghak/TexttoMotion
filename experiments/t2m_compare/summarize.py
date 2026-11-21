#!/home/jong/isaaclab/.venv/bin/python
"""Tables of the comparison with text-to-motion models: numbers stated in set 8, and physics over all outputs.

Usage on this computer:
    ./experiments/t2m_compare/summarize.py momask            # T2M outputs in out/<method>/ and out/<method>_plain/
    ./experiments/t2m_compare/summarize.py ours <exp_dir>     # our set-8 policies: out/ours_set8_<exp>_*

For a T2M method: out/<method>/<set>_<id>_r<k>.npy (HumanML3D joints, measure.py) and out/<method>_plain/*.npy (the
method's plain walk, "A person walks forward.", the reference of the angle changes). Writes
out/<method>_measures.json and out/<method>_report.md.
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

import measure as ms  # noqa: E402

SET8 = ROOT / "experiments" / "style_llm" / "test_commands_8.json"
# measure name of set 8 -> (feature of measure.py, taken as a change from the plain walk?)
# The lean commands are also read above the waist (upper_lean, measure.py), listed separately.
UPPER = {"torso_lean_change": ("upper_lean", True)}
MEASURES = {"torso_lean_change": ("torso_lean", True), "head_pitch_change": ("head_pitch", True),
            "cadence": ("cadence", False), "speed": ("speed", False),
            "step_length_ratio": ("step_length_m", "ratio"), "knee_bend_change": ("knee_bend", True),
            "arm_flexion": ("arm_flexion", True), "arm_abduction": ("arm_abduction", True),
            "leg_abduction_change": ("leg_abduction", True), "toe_out_change": ("toe_out", True)}
PHYSICS = ("penetration_cm", "floating_cm", "slide_cm", "skate")


def stated_value(measured: dict, plain: dict, measure: str, table: dict = MEASURES) -> float:
    feature, change = table[measure]
    value = measured.get(feature, float("nan"))
    if change == "ratio":
        return value / plain[feature]
    return value - plain[feature] if change else value


def upper_table(commands: list, values: dict) -> list:
    """Lines of the lean commands read above the waist; values {command id: [measured changes]}."""
    lines = ["", "## 상체 기울기, 허리 위로 잰 값", "",
             "허리(우리 몸통 관절, HumanML3D spine2)에서 목까지의 선이 수직에서 앞으로 기운 각도를 기본 걷기와 비교한 값이다.", "",
             "| ID | 명령 | 말한 값 | 잰 값 | 평균 오차 |", "| --- | --- | --- | --- | --- |"]
    for c in commands:
        if c["measure"] not in UPPER or c["id"] not in values:
            continue
        vals = values[c["id"]]
        finite = [v for v in vals if np.isfinite(v)]
        err = float(np.mean([abs(v - c["value"]) for v in finite])) if finite else float("nan")
        lines.append(f"| {c['id']} | {c['text']} | {c['value']} | " + ", ".join(f"{v:.2f}" for v in vals) + f" | {err:.2f} |")
    return lines


def summarize_t2m(method: str) -> int:
    out_dir = HERE / "out"
    plain_rows = [ms.measure_hml(Path(f)) for f in sorted(glob.glob(str(out_dir / f"{method}_plain" / "*.npy")))]
    plain = {k: float(np.nanmedian([r.get(k, np.nan) for r in plain_rows])) for k in
             ("torso_lean", "upper_lean", "head_pitch", "cadence", "speed", "step_length_m", "knee_bend",
              "arm_flexion", "arm_abduction", "leg_abduction", "toe_out")}
    rows = {}
    for f in sorted(glob.glob(str(out_dir / method / "*.npy"))):
        rows[Path(f).stem] = ms.measure_hml(Path(f))
    commands = json.loads(SET8.read_text())["commands"]
    lines = [f"# {method}: 수치를 말한 명령 (8세트)", "",
             f"각도 변화는 같은 모델의 기본 걷기(\"A person walks forward.\", 6초 10개, 중앙값)와의 차이이다. "
             f"기본 걷기: 속도 {plain['speed']:.2f} m/s, 박자 {plain['cadence']:.0f}걸음/분, 보폭 {plain['step_length_m']:.2f} m, "
             f"상체 {plain['torso_lean']:.1f}°.", "",
             "| ID | 명령 | 말한 값 | 잰 값 (3개) | 평균 오차 |", "| --- | --- | --- | --- | --- |"]
    errors = {}
    for c in commands:
        if c["measure"] == "plain":
            continue
        vals = []
        for k in range(10):
            r = rows.get(f"set8_{c['id']}_r{k}")
            if r is None:
                continue
            vals.append(stated_value(r, plain, c["measure"]) if "error" not in r else float("nan"))
        finite = [v for v in vals if np.isfinite(v)]
        err = float(np.mean([abs(v - c["value"]) for v in finite])) if finite else float("nan")
        errors[c["id"]] = {"stated": c["value"], "measured": vals, "abs_error": err}
        shown = ", ".join(f"{v:.2f}" if np.isfinite(v) else "-" for v in vals)
        lines.append(f"| {c['id']} | {c['text']} | {c['value']} | {shown} | {err:.2f} |")
    upper = {c["id"]: [stated_value(r, plain, c["measure"], UPPER) if "error" not in r else float("nan")
                       for k in range(10) for r in [rows.get(f"set8_{c['id']}_r{k}")] if r is not None]
             for c in commands if c["measure"] in UPPER}
    lines += upper_table(commands, upper)
    lines += ["", "## 물리 지표 (모든 출력)", "",
              "| 묶음 | 동작 수 | 땅 뚫기 (cm) | 떠 있음 (cm) | 디딘 발 미끄러짐 (cm, 중앙값) | 빠른 미끄러짐 비율 |",
              "| --- | --- | --- | --- | --- | --- |"]
    groups = {"8세트": [r for k, r in rows.items() if k.startswith("set8_")],
              "6세트": [r for k, r in rows.items() if k.startswith("set6_")],
              "7세트": [r for k, r in rows.items() if k.startswith("set7_")],
              "9세트": [r for k, r in rows.items() if k.startswith("set9_")],
              "10세트": [r for k, r in rows.items() if k.startswith("set10_")], "기본 걷기": plain_rows}
    groups = {name: group for name, group in groups.items() if group}
    physics = {}
    for name, group in groups.items():
        stats = {m: float(np.nanmean([r[m] for r in group])) if m != "slide_cm" else
                 float(np.nanmedian([r[m] for r in group])) for m in PHYSICS}
        physics[name] = {**stats, "n": len(group)}
        lines.append(f"| {name} | {len(group)} | {stats['penetration_cm']:.2f} | {stats['floating_cm']:.2f} | "
                     f"{stats['slide_cm']:.2f} | {stats['skate']:.3f} |")
    (out_dir / f"{method}_measures.json").write_text(json.dumps(
        {"plain": plain, "set8": errors, "physics": physics, "rows": rows}, indent=1, default=float))
    (out_dir / f"{method}_report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


def summarize_ours(exp_dir: Path) -> int:
    """Our set-8 policies: rollouts of experiments/style_eval/rollouts/<exp>__<key>.npz (4 characters x 30 s each),
    against our plain walk policy (the same base as every walk experiment)."""
    rollouts = ROOT / "experiments" / "style_eval" / "rollouts"
    base = ms.measure_ours(rollouts / "20261015_151030_walk_behaviors__base.npz")
    plain = {k: float(np.nanmedian([r.get(k, np.nan) for r in base])) for k in
             ("torso_lean", "upper_lean", "head_pitch", "cadence", "speed", "step_length_m", "knee_bend",
              "arm_flexion", "arm_abduction", "leg_abduction", "toe_out")}
    variants = {v["key"]: v for v in json.loads((exp_dir / "variants.json").read_text())}
    commands = {c["id"]: c for c in json.loads(SET8.read_text())["commands"]}
    lines = [f"# 우리 방법: 수치를 말한 명령 (8세트, {exp_dir.name})", "",
             f"학습한 정책을 캐릭터 4개로 30초씩 기록하여 잰 값이다. 각도 변화는 우리 기본 걷기 정책과의 차이이다. 기본 걷기: "
             f"속도 {plain['speed']:.2f} m/s, 박자 {plain['cadence']:.0f}걸음/분, 보폭 {plain['step_length_m']:.2f} m.", "",
             "| ID | 명령 | LLM이 정한 값 | 말한 값 | 잰 값 (캐릭터 4개) | 평균 오차 |", "| --- | --- | --- | --- | --- | --- |"]
    errors, rows = {}, {}
    for key, v in variants.items():
        if key == "base":
            continue
        cid = v["source"]["id"]
        c = commands[cid]
        result = ms.measure_ours(rollouts / f"{exp_dir.name}__{key}.npz")
        rows[cid] = result
        vals = [stated_value(r, plain, c["measure"]) if "error" not in r else float("nan") for r in result]
        finite = [x for x in vals if np.isfinite(x)]
        err = float(np.mean([abs(x - c["value"]) for x in finite])) if finite else float("nan")
        errors[cid] = {"stated": c["value"], "measured": vals, "abs_error": err}
        shown = ", ".join(f"{x:.2f}" if np.isfinite(x) else "-" for x in vals)
        answer = v["label"].split("이 정한 값 (")[-1].rstrip(")")
        lines.append(f"| {cid} | {c['text']} | {answer} | {c['value']} | {shown} | {err:.2f} |")
    upper = {cid: [stated_value(r, plain, commands[cid]["measure"], UPPER) if "error" not in r else float("nan")
                   for r in result] for cid, result in rows.items() if commands[cid]["measure"] in UPPER}
    lines += upper_table(list(commands.values()), upper)
    allrows = [r for result in rows.values() for r in result]
    stats = {m: float(np.nanmean([r[m] for r in allrows])) if m != "slide_cm" else
             float(np.nanmedian([r[m] for r in allrows])) for m in PHYSICS}
    lines += ["", f"물리 지표 ({len(allrows)}개 기록): 땅 뚫기 {stats['penetration_cm']:.3f} cm, 떠 있음 {stats['floating_cm']:.3f} cm, "
                  f"디딘 발 미끄러짐 중앙값 {stats['slide_cm']:.2f} cm, 빠른 미끄러짐 비율 {stats['skate']:.3f}"]
    out = HERE / "out"
    (out / f"ours_set8_{exp_dir.name}_measures.json").write_text(json.dumps(
        {"plain": plain, "set8": errors, "physics": stats, "rows": rows}, indent=1, default=float))
    (out / f"ours_set8_{exp_dir.name}_report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


def main() -> int:
    if sys.argv[1] == "ours":
        return summarize_ours(Path(sys.argv[2]).resolve())
    return summarize_t2m(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
