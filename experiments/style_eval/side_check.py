#!/home/jong/isaaclab/.venv/bin/python
"""One-sided checks of set 9 (experiments/style_llm/test_commands_9.json) on the style targets of an LLM run, without
training: every accepted answer's target motion (target_features.py) gives the one-sided measures of
gait_features.features()["_side"], and the command's check expression must reach its min. The sideways tilts
(torso_roll, head_roll) are read as changes from the same method's plain walk.

Usage on this computer:
    ./experiments/style_eval/side_check.py experiments/style_llm/<run of set 9>
    ./experiments/style_eval/side_check.py --trained experiments/style_walk/<experiment>   # trained policies
    ./experiments/style_eval/side_check.py --hml momask    # a text-to-motion model (experiments/t2m_compare/out)

Writes <run>/style_side.json (the sets), <run>/style_side_targets.json (features) and <run>/side_check.md. With
--trained, the recorded rollouts (record_policies.py: 4 characters x 30 s) of every variant are measured per
character, the set-9 checks are applied to the variants that came from set 9, and every variant's one-sided measures
are listed against the plain walk policy's (with the heel raise for walking on the toes); writes
<experiment>/side_check.md and .json.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SET9 = ROOT / "experiments" / "style_llm" / "test_commands_9.json"


TILTS = ("torso_roll", "head_roll")  # absolute angles: read as the change from the same method's plain walk


def relative(side: dict, plain: dict) -> dict:
    """The one-sided measures with the sideways tilts taken as changes from the plain walk (a skeleton's rest pose
    may already tilt its head; HumanML3D's plain walks measure a head_roll of about 8 degrees)."""
    return {**side, **{name: side[name] - plain[name] for name in TILTS}}


def check_value(expr: str, side: dict, named: dict) -> float:
    """The value of a check expression over the one-sided measures (and the named checks of the set)."""
    space = {"abs": abs, "max": max, "min": min, **side}
    for name, text in named.items():
        space[name] = eval(text, {"__builtins__": {}}, dict(space))  # noqa: S307 - expressions of our own test set
    return float(eval(expr, {"__builtins__": {}}, space))  # noqa: S307


def rollout_sides(path: Path) -> list:
    """One-sided measures of each character of a recorded rollout (after its last reset, as measure.py does)."""
    import numpy as np

    sys.path.insert(0, str(HERE))
    import gait_features as gf

    data = np.load(path, allow_pickle=True)
    names, fps, out = list(data["body_names"]), 1.0 / float(data["dt"]), []
    for n in range(data["body_pos"].shape[1]):
        resets = np.nonzero(data["reset"][:, n])[0]
        start = int(resets[-1]) + 5 if len(resets) and resets[-1] > 5 else 0
        points = gf.sim_points(data["body_pos"][start:, n].astype(np.float64), data["body_rot"][start:, n].astype(np.float64), names)
        try:
            out.append(gf.features(points, fps)["_side"])
        except ValueError:
            out.append(None)
    return out


def check_trained(exp: Path) -> int:
    import numpy as np

    spec = json.loads(SET9.read_text())
    commands = {c["id"]: c for c in spec["commands"]}
    rollouts = HERE / "rollouts"
    base = [s for s in rollout_sides(rollouts / "20261015_151030_walk_behaviors__base.npz") if s]
    mean = lambda rows, name: float(np.mean([r[name] for r in rows]))  # noqa: E731
    plain = {name: mean(base, name) for name in base[0]}
    lines = [f"# 한쪽 동작 확인, 학습한 정책 ({exp.name})", "",
             "캐릭터 4개를 30초씩 기록하여 캐릭터마다 잰 값이다. 기본 걷기는 모든 걷기 실험의 기본 정책이다.", "",
             "| 변형 | 확인 식 | 기준 | 값 (캐릭터 4개) | 기본 걷기 | 결과 |", "| --- | --- | --- | --- | --- | --- |"]
    results = {}
    for v in json.loads((exp / "variants.json").read_text()):
        if v["key"] == "base" or not (rollouts / f"{exp.name}__{v['key']}.npz").exists():
            continue
        sides = [s for s in rollout_sides(rollouts / f"{exp.name}__{v['key']}.npz") if s]
        results[v["key"]] = {"label": v["label"], "per_character": sides,
                             "mean": {name: mean(sides, name) for name in sides[0]} if sides else None}
        cid = (v.get("source") or {}).get("id")
        if cid in commands:
            c = commands[cid]
            values = [check_value(c["check"], relative(s, plain), spec["checks"]) for s in sides]
            ok = sum(x >= c["min"] for x in values)
            results[v["key"]].update(check=c["check"], values=values, passed=ok)
            lines.append(f"| {v['key']} ({c['text']}) | `{c['check']}` | {c['min']:g} | "
                         + ", ".join(f"{x:.2f}" for x in values) + f" | {check_value(c['check'], relative(plain, plain), spec['checks']):.2f} | "
                         f"{ok}/{len(values)} 통과 |")
    lines += ["", "## 한쪽 값 (캐릭터 4개 평균, 기본 걷기와의 차이)", "",
              "| 변형 | 상체 옆 기울기 (°, + 오른쪽) | 고개 옆 기울기 (°) | 무릎 범위 오른쪽/왼쪽 (°) | 손 높이 오른쪽/왼쪽 (팔 길이) | "
              "발뒤꿈치 들림 오른쪽/왼쪽 (다리 길이) |", "| --- | --- | --- | --- | --- | --- |"]
    for key, r in results.items():
        m = r["mean"]
        if not m:
            lines.append(f"| {key} | 잴 수 없음 | | | | |")
            continue
        d = {name: m[name] - plain[name] for name in m}
        lines.append(f"| {key} | {d['torso_roll']:+.1f} | {d['head_roll']:+.1f} | {d['r_knee_range']:+.1f} / {d['l_knee_range']:+.1f} | "
                     f"{d['r_hand_height']:+.2f} / {d['l_hand_height']:+.2f} | {d['r_heel_raise']:+.3f} / {d['l_heel_raise']:+.3f} |")
    (exp / "side_check.json").write_text(json.dumps({"plain": plain, "variants": results}, ensure_ascii=False, indent=1))
    (exp / "side_check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


def check_hml(method: str) -> int:
    """The set-9 checks on a text-to-motion model's outputs (3 per command), against its own plain walk."""
    import glob

    import numpy as np

    sys.path.insert(0, str(HERE))
    sys.path.insert(0, str(ROOT / "experiments" / "t2m_compare"))
    import gait_features as gf
    import measure as ms

    out_dir = ROOT / "experiments" / "t2m_compare" / "out"

    def sides(path):
        joints = np.load(path)
        joints = joints[0] if joints.ndim == 4 else joints
        try:
            return gf.features(ms.hml_points(joints), ms.HML_FPS, min_frames=int(2 * ms.HML_FPS))["_side"]
        except ValueError:
            return None

    plain_rows = [x for x in (sides(f) for f in sorted(glob.glob(str(out_dir / f"{method}_plain" / "*.npy")))) if x]
    plain = {name: float(np.median([r[name] for r in plain_rows])) for name in plain_rows[0]}
    spec = json.loads(SET9.read_text())
    lines = [f"# 한쪽 동작 확인, {method} (출력 3개씩)", "",
             "명령마다 3개의 출력에서 잰 값이다. 곧게 걷지 못해 잴 수 없는 출력은 -로 적었다.", "",
             "| ID | 명령 | 확인 식 | 기준 | 값 (출력 3개) | 기본 걷기 | 통과 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    results, passed = {}, 0
    for c in spec["commands"]:
        values = []
        for f in sorted(glob.glob(str(out_dir / method / f"set9_{c['id']}_r*.npy"))):
            side = sides(f)
            values.append(check_value(c["check"], relative(side, plain), spec["checks"]) if side else float("nan"))
        ok = sum(v >= c["min"] for v in values if np.isfinite(v))
        passed += ok
        results[c["id"]] = {"values": values, "passed": ok}
        shown = ", ".join(f"{v:.2f}" if np.isfinite(v) else "-" for v in values)
        lines.append(f"| {c['id']} | {c['text']} | `{c['check']}` | {c['min']:g} | {shown} | "
                     f"{check_value(c['check'], relative(plain, plain), spec['checks']):.2f} | {ok}/{len(values)} |")
    total = sum(len(r["values"]) for r in results.values())
    lines += ["", f"통과 {passed}/{total}"]
    (out_dir / f"{method}_side_check.json").write_text(json.dumps(results, indent=1))
    (out_dir / f"{method}_side_check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


def main() -> int:
    if sys.argv[1] == "--hml":
        return check_hml(sys.argv[2])
    if sys.argv[1] == "--trained":
        return check_trained(Path(sys.argv[2]).resolve())
    run = Path(sys.argv[1]).resolve()
    spec = json.loads(SET9.read_text())
    rows = json.loads((run / "results.json").read_text())["results"]
    sets = [{"key": "base", "scales": {}}] + [{"key": r["id"], "scales": r["scales"]} for r in rows
                                              if "scales" in r and r["params"]["action"] == "walk"]
    sets_file = run / "style_side.json"
    sets_file.write_text(json.dumps(sets, ensure_ascii=False, indent=1))
    proc = subprocess.run([str(HERE / "target_features.py"), str(sets_file)], cwd=ROOT)
    feats = json.loads((run / "style_side_targets.json").read_text())
    if proc.returncode != 0:
        return proc.returncode
    base = feats["base"]["_side"]
    lines = [f"# 한쪽 동작 확인 ({run.name}, 학습 없이 목표 동작으로)", "",
             "값이 기준 이상이면 통과이다. 기본 걷기 열은 같은 식을 보통 걸음의 목표 동작에 적용한 값이다.", "",
             "| ID | 명령 | 답 | 확인 식 | 기준 | 값 | 기본 걷기 | 결과 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    passed, results = 0, []
    sys.path.insert(0, str(ROOT / "experiments" / "style_llm"))
    import style_parser as sp
    for command in spec["commands"]:
        row = next(r for r in rows if r["id"] == command["id"])
        answer = sp.compact(row["params"]) if "params" in row else f"거절 ({row.get('rejection')})"
        side = (feats.get(command["id"]) or {}).get("_side")
        value = check_value(command["check"], relative(side, base), spec["checks"]) if side else float("nan")
        plain = check_value(command["check"], relative(base, base), spec["checks"])
        ok = value >= command["min"]
        passed += ok
        results.append({"id": command["id"], "value": value, "plain": plain, "pass": bool(ok), "side": side})
        lines.append(f"| {command['id']} | {command['text']} | {answer} | `{command['check']}` | {command['min']:g} | "
                     f"{value:.2f} | {plain:.2f} | {'통과' if ok else '실패'} |")
    lines += ["", f"통과 {passed}/{len(spec['commands'])}"]
    (run / "side_check.json").write_text(json.dumps(results, indent=1))
    (run / "side_check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
