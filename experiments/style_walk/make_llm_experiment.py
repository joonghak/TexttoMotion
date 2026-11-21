#!/home/jong/isaaclab/.venv/bin/python
"""An experiment folder for run_style_walk.py --resume from the answers of one LLM run (experiments/style_llm/<run>).

Usage on this computer:
    ./experiments/style_walk/make_llm_experiment.py experiments/style_llm/<run> N3,N4,P5 --prefix v6 --name v6_set6
    ./experiments/style_walk/run_style_walk.py --resume experiments/style_walk/<새 폴더> --iters 2000 --only v6_N3,...

The folder gets variants.json with the answers' scales (as the LLM run wrote them in its variants.json), each labelled
with the command, the model and the prompt version that chose the values, and `base` as a link to the plain walk
policy that every walk experiment uses (20261006_234135/s1). Nothing is trained here.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "style_llm"))

BASE = "../20261006_234135/s1"


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("run", type=Path, help="LLM 실행 폴더 (results.json, variants.json)")
    cli.add_argument("ids", help="쉼표로 구분한 명령 ID")
    cli.add_argument("--prefix", required=True, help="변형 key 앞부분 (예: v6 -> v6_N3)")
    cli.add_argument("--name", required=True, help="폴더 이름 뒷부분")
    args = cli.parse_args()
    import style_parser as sp

    run = args.run.resolve()
    summary = json.loads((run / "results.json").read_text())
    rows = {row["id"]: row for row in summary["results"]}
    trained = {v["key"]: v for v in json.loads((run / "variants.json").read_text())}
    who = f"{summary['model'].split('/')[-1]}, 프롬프트 {summary['prompt']}"
    variants = [{"key": "base", "label": "기본 걷기", "scales": {}}]
    for cid in [c.strip() for c in args.ids.split(",") if c.strip()]:
        if cid not in trained:
            print(f"{cid}: 수락된 걷기 답이 없습니다", file=sys.stderr)
            return 1
        row = rows[cid]
        entry = {"key": f"{args.prefix}_{cid}",
                 "label": f"{row['text']}: {who}이 정한 값 ({sp.compact(row['params'])})",
                 "scales": trained[cid]["scales"], "source": {"run": run.name, "id": cid, "target": row.get("target")}}
        if trained[cid].get("clip", "walk") != "walk":
            entry["clip"] = trained[cid]["clip"]
        variants.append(entry)
    out = HERE / (datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{args.name}")
    out.mkdir()
    (out / "base").symlink_to(BASE)
    (out / "variants.json").write_text(json.dumps(variants, ensure_ascii=False, indent=1))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
