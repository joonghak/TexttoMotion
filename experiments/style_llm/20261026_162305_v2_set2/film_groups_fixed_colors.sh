#!/usr/bin/env bash
# The first group films took their colours from the folder order, so A6, B2 and B8 came out blue like base.
# Same groups again with base blue and the others in group order: 0 파랑, 1 초록, 2 노랑, 3 빨강, 4 보라, 5 검정.
set -uo pipefail
D=experiments/style_llm/20261026_162305_v2_set2
FILM=experiments/style_walk/film.py
"$FILM" "$D" --variants base,A6,A8,A9,A10 --colors 0,1,2,3,4 --name group_a2 || echo "FAILED group_a2"
"$FILM" "$D" --variants base,B1,B2,B3,B4,B6 --colors 0,1,2,3,4,5 --name group_b1 || echo "FAILED group_b1"
"$FILM" "$D" --variants base,B8,B9,B10 --colors 0,1,2,3 --name group_b2 || echo "FAILED group_b2"
echo "done"
