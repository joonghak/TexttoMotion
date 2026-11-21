#!/home/jong/isaaclab/.venv/bin/python
"""Gait features of the 100STYLE forward walks (FW), the reference for style_metric.py.

Usage on this computer (the BVH files are not in the repo; see README.md for the download):
    ./experiments/style_eval/build_reference.py [--data /home/jong/datasets/100STYLE]

Writes experiments/style_eval/reference_100style.json: per style the features of its forward walk (frames cut with
Frame_Cuts.csv) and its difference from Neutral; and per feature the spread of those differences over the 99 styles,
used to put the features on one scale.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import gait_features as gf  # noqa: E402

OUT = HERE / "reference_100style.json"


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    cli.add_argument("--data", default="/home/jong/datasets/100STYLE", help="100STYLE 폴더 (FW/*.bvh, raw/Frame_Cuts.csv)")
    args = cli.parse_args()
    data = Path(args.data)
    cuts = {row["STYLE_NAME"]: row for row in csv.DictReader(open(data / "raw" / "Frame_Cuts.csv"))}
    styles = {}
    for name in sorted(cuts):
        path = data / "FW" / f"{name}_FW.bvh"
        row = cuts[name]
        try:
            points, fps = gf.bvh_points(path, int(row["FW_START"]), int(row["FW_STOP"]))
            styles[name] = gf.features(points, fps)
        except (ValueError, FileNotFoundError) as exc:
            print(f"skip {name}: {exc}", file=sys.stderr)
            continue
        print(f"{name}: {styles[name]['_frames']} frames, {styles[name]['_speed']:.2f} m/s", file=sys.stderr)
    plain = dict(styles["Neutral"])
    # The Neutral clip turns the right foot in by about 15 degrees (toe_out at the 3rd percentile of the 100 clips,
    # while plain styles such as Proud, Angry or March sit near the middle), so toe_out is measured from the median
    # of all clips instead; every other feature from Neutral.
    plain["toe_out"] = float(np.median([f["toe_out"] for f in styles.values()]))
    deltas = {name: gf.style_delta(f, plain) for name, f in styles.items() if name != "Neutral"}
    matrix = np.stack(list(deltas.values()))
    scale = np.nanstd(matrix, axis=0)
    result = {"source": "100STYLE (Mason, Starke and Komura 2022), forward walks, CC BY 4.0",
              "features": {name: meaning for name, (meaning, _) in gf.FEATURES.items()},
              "scale": dict(zip(gf.FEATURES, scale.round(6).tolist())),
              "plain": "Neutral (toe_out: median of all 100 clips, the Neutral clip turns the right foot in)",
              "plain_features": {k: round(v, 6) for k, v in plain.items()},
              "styles": {name: {"features": {k: round(v, 6) for k, v in f.items()},
                                "delta": dict(zip(gf.FEATURES, deltas[name].round(6).tolist())) if name in deltas else None}
                         for name, f in styles.items()}}
    OUT.write_text(json.dumps(result, indent=1))
    print(f"{len(styles)} styles -> {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
