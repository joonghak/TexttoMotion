#!/usr/bin/env bash
# Level 3 of set 2: group videos with close-ups, one quarter-view video per command, then quality_eval.
# Run from the repository root: experiments/style_llm/20261026_162305_v2_set2/film_all.sh
set -uo pipefail
D=experiments/style_llm/20261026_162305_v2_set2
FILM=experiments/style_walk/film.py
step() { echo "=== $(date +%H:%M:%S) $*"; }

# Side view, base (blue) first in every group, then the commands in ID order.
for group in "a1:base,A1,A2,A3,A4,A5" "a2:base,A6,A8,A9,A10" "b1:base,B1,B2,B3,B4,B6" "b2:base,B8,B9,B10"; do
    name=${group%%:*}; variants=${group#*:}
    step "group_$name ($variants)"
    "$FILM" "$D" --variants "$variants" --name "group_$name" || echo "FAILED group_$name"
done

# One character per video, 40 degrees off its path.
for key in A1 A2 A3 A4 A5 A6 A8 A9 A10 B1 B2 B3 B4 B6 B8 B9 B10; do
    step "solo_$key"
    "$FILM" "$D" --variants "$key" --view quarter --name "solo_$key" || echo "FAILED solo_$key"
done

step "quality_eval"
experiments/style_walk/quality_eval.py "$D" --variants base,A1,A2,A3,A4,A5,A6,A8,A9,A10,B1,B2,B3,B4,B6,B8,B9,B10 \
    || echo "FAILED quality_eval"
step "done"
