#!/home/jong/isaaclab/.venv/bin/python
"""Style metric of recorded policies against 100STYLE (record_policies.py first).

Usage on this computer:
    ./experiments/style_eval/evaluate_policies.py <set.json> [--out <report.md>]

set.json lists the policies: {"title": ..., "items": [{"label", "command", "rollout", "base", "target"}]}, where
rollout and base name .npz files in rollouts/ (the base is the plain walk of the same reference clip) and target is a
100STYLE style or null (then only the nearest styles are reported). Targets are fixed in the set before evaluation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import gait_features as gf  # noqa: E402
import style_metric as sm  # noqa: E402

ROLLOUTS = HERE / "rollouts"
MIN_SECONDS = 10.0


def rollout_features(name: str) -> dict:
    """Mean gait features over the characters of a recording, each cut into segments between resets."""
    data = np.load(ROLLOUTS / f"{name}.npz")
    pos, rot, reset = data["body_pos"], data["body_rot"], data["reset"]
    names, fps = [str(n) for n in data["body_names"]], 1.0 / float(data["dt"])
    found = []
    for n in range(pos.shape[1]):
        cuts = [0] + [int(t) + 1 for t in np.nonzero(reset[:, n])[0]] + [len(pos)]
        for start, stop in zip(cuts[:-1], cuts[1:]):
            if stop - start >= MIN_SECONDS * fps:
                try:
                    found.append(gf.features(gf.sim_points(pos[start:stop, n], rot[start:stop, n], names), fps))
                except ValueError:
                    pass
    if not found:
        raise ValueError(f"{name}: no segment of {MIN_SECONDS} s")
    with np.errstate(all="ignore"):
        # "_side" (per-side measures, gait_features since prompt v11) is a dict, not a feature of the metric
        mean = {key: float(np.nanmean([f[key] for f in found])) for key in found[0] if not isinstance(found[0][key], dict)}
    mean["_segments"] = len(found)
    mean["_resets"] = int(reset.sum())
    return mean


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("set", type=Path)
    cli.add_argument("--out", type=Path, help="결과 표 (기본: set 파일 옆 <이름>_report.md)")
    args = cli.parse_args()
    spec = json.loads(args.set.read_text())
    ref = sm.Reference()
    cache, rows, results = {}, [], []

    def feats(name):
        if name not in cache:
            cache[name] = rollout_features(name)
        return cache[name]

    for item in spec["items"]:
        delta = gf.style_delta(feats(item["rollout"]), feats(item["base"]))
        result = ref.evaluate(delta, target=item.get("target"), top=3)
        results.append({**item, **result, "delta": dict(zip(gf.FEATURES, np.round(delta, 4).tolist()))})
        top = ", ".join(f"{name} {sim:.2f}" for name, sim in result["top"])
        size = float(np.linalg.norm(np.nan_to_num(ref.scaled(delta))))
        results[-1]["size"] = round(size, 3)
        if item.get("target"):
            rows.append(f"| {item['label']} | {item['command']} | {item['target']} | {result['similarity']:.2f} | "
                        f"{result['rank']} | {result['strength']:.2f} | {size:.1f} | {top} |")
        else:
            rows.append(f"| {item['label']} | {item['command']} | - | - | - | - | {size:.1f} | {top} |")
    targeted = [r for r in results if r.get("target")]
    lines = [f"# {spec['title']}", "",
             "유사도: 우리 정책이 기본 걸음에서 달라진 방향과 100STYLE 스타일이 Neutral에서 달라진 방향의 코사인 "
             "(특징마다 100STYLE 99종의 차이 분포로 나눈 뒤). 순위: 99종 가운데 목표 스타일의 순위. 크기: 우리 차이의 길이 / "
             f"목표 스타일 차이의 길이. 변화: 우리 차이의 길이(같은 단위, 100STYLE 99종의 중앙값 "
             f"{np.median(np.linalg.norm(np.nan_to_num(ref.deltas), axis=1)):.1f}).", "",
             "| 정책 | 명령 | 목표 (100STYLE) | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"] + rows
    if targeted:
        lines += ["", f"목표가 있는 {len(targeted)}개: 유사도 평균 {np.mean([r['similarity'] for r in targeted]):.2f}, "
                      f"1위 {sum(r['rank'] == 1 for r in targeted)}개, 5위 이내 {sum(r['rank'] <= 5 for r in targeted)}개, "
                      f"크기 평균 {np.mean([r['strength'] for r in targeted]):.2f}"]
    out = args.out or args.set.with_name(args.set.stem + "_report.md")
    out.write_text("\n".join(lines) + "\n")
    out.with_suffix(".json").write_text(json.dumps({"results": results,
                                                    "features": {k: v for k, v in cache.items()}}, indent=1))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
