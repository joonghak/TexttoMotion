#!/usr/bin/env bash
# Level 3 of prompt v3 on set 2: each retrained command beside the plain walk and its v2 policy (when v2 trained one),
# a quarter view of each v3 policy, then quality_eval. Run from the repository root after the training:
#   experiments/style_llm/20261027_192233_v3_set2/film_all.sh
# Colours: 0 파랑 base (plain walk), 1 초록 v2, 3 빨강 v3.
set -uo pipefail
D=experiments/style_llm/20261027_192233_v3_set2
KEYS="${KEYS:-A10 B9 A8 B7}"  # KEYS=A10 NO_EVAL=1 film_all.sh films one policy while the next one trains
FILM=experiments/style_walk/film.py
step() { echo "=== $(date +%H:%M:%S) $*"; }
trained() { [ -f "$D/$1/train/model.pt" ]; }
filmed() { [ -f "$D/film/$1.mp4" ]; }  # filmed earlier, while the last policy trained

for key in $KEYS; do
    trained "$key" || { echo "skip $key (not trained)"; continue; }
    filmed "pair_$key" && continue
    step "pair_$key"
    if [ -e "$D/${key}_v2" ]; then
        "$FILM" "$D" --variants "base,${key}_v2,$key" --colors 0,1,3 --name "pair_$key" || echo "FAILED pair_$key"
    else
        "$FILM" "$D" --variants "base,$key" --colors 0,3 --name "pair_$key" || echo "FAILED pair_$key"
    fi
done
for key in $KEYS; do
    trained "$key" || continue
    filmed "solo_${key}_v3_quarter" && continue
    step "solo_${key}_v3"
    "$FILM" "$D" --variants "$key" --view quarter --name "solo_${key}_v3" || echo "FAILED solo_${key}_v3"
done
[ -n "${NO_EVAL:-}" ] && { step "done"; exit 0; }
done_keys=$(for key in $KEYS; do trained "$key" && printf ",%s" "$key"; done)
step "quality_eval"
experiments/style_walk/quality_eval.py "$D" --variants "base$done_keys" || echo "FAILED quality_eval"
step "done"
