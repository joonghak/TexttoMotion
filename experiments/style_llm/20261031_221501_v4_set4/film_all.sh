#!/usr/bin/env bash
# Videos and measurements of the set-4 policies, one reference clip at a time (one simulation loads one clip).
# Run from the repository root after the training: experiments/style_llm/20261031_221501_v4_set4/film_all.sh
# Group videos: base of that clip first (0 파랑), then the commands in the order below (1 초록, 2 노랑, 3 빨강, 4 보라, 5 검정).
set -uo pipefail
D=experiments/style_llm/20261031_221501_v4_set4
FILM=experiments/style_walk/film.py
step() { echo "=== $(date +%H:%M:%S) $*"; }
trained() { [ -f "$D/$1/train/model.pt" ]; }
NEW=""

for group in "run:B1 B2 A2 A6 A10" "jump:A3 A4 B3 B6" "kick:B4 B5"; do
    clip=${group%%:*}; keys=""
    for key in ${group#*:}; do trained "$key" && keys="$keys,$key"; done
    [ -z "$keys" ] && continue
    variants="base_$clip$keys"
    colors=$(seq -s, 0 $(( $(tr -cd , <<< "$variants" | wc -c) )))
    step "group_$clip ($variants)"
    "$FILM" "$D" --variants "$variants" --colors "$colors" --name "group_$clip" || echo "FAILED group_$clip"
    step "quality_eval $clip"
    experiments/style_walk/quality_eval.py "$D" --variants "$variants" || echo "FAILED quality_eval $clip"
    mkdir -p "$D/quality_$clip" && cp "$D"/quality/* "$D/quality_$clip/" 2>/dev/null
done
for key in B1 B2 B3 B4 B5 B6 A4 A2 A10 A6; do
    trained "$key" || continue
    [ -L "$D/$key" ] && continue  # reused policies were filmed in their own folders
    step "solo_$key"
    "$FILM" "$D" --variants "$key" --view quarter --name "solo_$key" || echo "FAILED solo_$key"
done
step "done"
