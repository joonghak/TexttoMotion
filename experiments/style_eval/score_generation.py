#!/home/jong/isaaclab/.venv/bin/python
"""Style metric of an LLM generation run without training: the style targets of its parameters against 100STYLE.

Usage on this computer:
    ./experiments/style_eval/score_generation.py experiments/style_llm/<시각>_v6_set6 [...]

For every accepted walk command of the run (results.json of style_parser.py --test) the scales it produced are
played as style targets (target_features.py) and compared with the command's 100STYLE target (the "target" of the
test set). Writes <run>/style_metric.md and .json. Commands without a target or not on the walk are listed only.
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

import gait_features as gf  # noqa: E402
import style_metric as sm  # noqa: E402


def remap_rows(data: dict) -> None:
    """Feature answers (v6 to v8) mapped again with the latest mapping (FEATURE_LEVELS_V8), in place."""
    import style_parser as sp

    for row in data["results"]:
        if "params" not in row or "features" not in row["params"]:
            continue
        params = sp.validate_v8(row["answer"])  # the latest mapping
        row["rules"] = sp.companion_rules(params)
        row["params"], row["scales"] = params, sp.to_scales(params)


def score(run_dir: Path, ref: sm.Reference, remap: bool = False) -> dict:
    data = json.loads((run_dir / "results.json").read_text())
    tag = "_remap" if remap else ""
    if remap:
        remap_rows(data)
    sets_file = run_dir / f"style_targets{tag}.json"
    sets = [{"key": "_base", "scales": {}}]
    rows = []
    for row in data["results"]:
        if "scales" in row and row["params"]["action"] == "walk" and row.get("target"):
            sets.append({"key": row["id"], "scales": row["scales"]})
        rows.append(row)
    sets_file.write_text(json.dumps(sets, ensure_ascii=False, indent=1))
    proc = subprocess.run([str(HERE / "target_features.py"), str(sets_file)], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    targets_file = run_dir / f"style_targets{tag}_targets.json"
    if proc.returncode != 0 or not targets_file.exists():
        raise RuntimeError(proc.stdout[-2000:])
    feats = json.loads(targets_file.read_text())
    out = []
    for row in rows:
        entry = {"id": row["id"], "text": row["text"], "target": row.get("target")}
        if row["id"] in feats and "error" not in feats[row["id"]]:
            delta = gf.style_delta(feats[row["id"]], feats["_base"])
            entry.update(ref.evaluate(delta, target=row["target"], top=3))
            entry["size"] = round(float(np.linalg.norm(np.nan_to_num(ref.scaled(delta)))), 2)
        entry["answer"] = row.get("rejection") or row.get("params")
        out.append(entry)
    return {"run": run_dir.name + tag, "prompt": data["prompt"], "results": out}


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("runs", nargs="+", type=Path)
    cli.add_argument("--remap", action="store_true",
                     help="v6/v7의 특징 답을 지금의 FEATURE_LEVELS로 다시 값으로 옮겨 채점 (LLM을 다시 돌리지 않음)")
    args = cli.parse_args()
    ref = sm.Reference()
    sys.path.insert(0, str(ROOT / "experiments" / "style_llm"))
    import style_parser as sp

    for run_dir in args.runs:
        result = score(run_dir.resolve(), ref, args.remap)
        scored = [r for r in result["results"] if "similarity" in r]
        lines = [f"# 스타일 지표, 목표 동작 기준 ({result['run']}, 프롬프트 {result['prompt']})", "",
                 "학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 "
                 "대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).", "",
                 "| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |",
                 "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in result["results"]:
            answer = r["answer"]
            shown = sp.compact({**{k: answer.get(k, d) for k, (_, _, d) in sp.PARAMS.items()},
                                "action": answer.get("action", "walk")}) if isinstance(answer, dict) else f"거절 ({answer})"
            if "similarity" in r:
                top = ", ".join(f"{n} {s:.2f}" for n, s in r["top"])
                lines.append(f"| {r['id']} | {r['text']} | {r['target']} | {r['similarity']:.2f} | {r['rank']} | "
                             f"{r['strength']:.2f} | {r['size']:.1f} | {top} | {shown} |")
            else:
                lines.append(f"| {r['id']} | {r['text']} | {r['target'] or '-'} | - | - | - | - | - | {shown} |")
        if scored:
            lines += ["", f"점수를 낸 {len(scored)}개: 유사도 평균 {np.mean([r['similarity'] for r in scored]):.2f}, "
                          f"1위 {sum(r['rank'] == 1 for r in scored)}개, 5위 이내 {sum(r['rank'] <= 5 for r in scored)}개, "
                          f"순위 중앙값 {np.median([r['rank'] for r in scored]):.0f}, 크기 평균 "
                          f"{np.mean([r['strength'] for r in scored]):.2f}"]
        tag = "_remap" if args.remap else ""
        (run_dir / f"style_metric{tag}.md").write_text("\n".join(lines) + "\n")
        (run_dir / f"style_metric{tag}.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
