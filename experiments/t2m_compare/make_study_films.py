#!/home/jong/isaaclab/.venv/bin/python
"""Blind videos for the human study: every chosen command filmed once per method, same character, colour and cameras.

Usage on this computer (after the final runs):
    ./experiments/t2m_compare/make_study_films.py 7:N1,N2,P5 8:Q1,Q4 9:S1 10:C2 [--seed 0] [--out study]
    ./experiments/style_eval/film_compare.py experiments/t2m_compare/study/films.json

For each command: our final policy (experiments/style_walk/*_f<set>_set<set>_final/f<set>_<id>) and the first output
(r<seed>) of MoMask, T2M-GPT and MDM on the same command, filmed together in film_compare's blind mode (one colour, no
names; the generated clips turned to walk along +x). Writes experiments/t2m_compare/study/films.json (the film spec)
and study/stimuli.json (--out names another folder under experiments/t2m_compare, e.g. for a trial run): per command the text, the four video files and a random order of the methods, labelled
A to D (the key that says which letter is ours stays in this file, not on the page shown to the raters).
"""

from __future__ import annotations

import glob
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METHODS = ("momask", "t2mgpt", "mdm")
SETS = {n: ROOT / "experiments" / "style_llm" / f"test_commands_{n}.json" for n in ("7", "8", "9", "10")}


def main() -> int:
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 0
    study = HERE / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "study")
    chosen = [a for a in sys.argv[1:] if ":" in a]
    rng = random.Random(20261116 + seed)
    study.mkdir(exist_ok=True)
    pairs, stimuli = [], []
    for item in chosen:
        set_name, ids = item.split(":")
        commands = {c["id"]: c for c in json.loads(SETS[set_name].read_text())["commands"]}
        exp = sorted(glob.glob(str(ROOT / "experiments" / "style_walk" / f"*_f{set_name}_set{set_name}_final")))
        if not exp:
            print(f"set {set_name}: no final experiment yet", file=sys.stderr)
            return 1
        exp = Path(exp[-1])
        variants = {v["key"]: v for v in json.loads((exp / "variants.json").read_text())}
        for cid in ids.split(","):
            key = f"f{set_name}_{cid}"
            if key not in variants or not (exp / key / "train" / "model.pt").exists():
                print(f"{key}: not trained", file=sys.stderr)
                return 1
            name = f"set{set_name}_{cid}"
            clips = [{"type": "hml", "file": str((HERE / "out" / m / f"{name}_r{seed}.npy").relative_to(ROOT)), "method": m}
                     for m in METHODS]
            seconds = 8.0 if variants[key].get("clip", "walk").startswith("chain_") else 6.0
            pairs.append({"key": name, "run": str((exp / key).relative_to(ROOT)), "ours": "", "clips": clips,
                          "seconds": seconds, "blind": True, "caption": ""})
            order = ["ours", *METHODS]
            rng.shuffle(order)
            stimuli.append({"key": name, "text": commands[cid]["text"],
                            "videos": {letter: f"{name}_{method}.mp4" for letter, method in zip("ABCD", order)},
                            "answer_key": dict(zip("ABCD", order))})
    (study / "films.json").write_text(json.dumps({"out": str((study / "videos").relative_to(ROOT)), "pairs": pairs},
                                                 ensure_ascii=False, indent=1))
    (study / "stimuli.json").write_text(json.dumps(stimuli, ensure_ascii=False, indent=1))
    print(f"{len(pairs)} commands -> {study / 'films.json'}, {study / 'stimuli.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
