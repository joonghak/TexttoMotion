#!/usr/bin/env bash
# Videos and measurements of the general-formula comparison, one reference clip at a time.
# Run from the repository root after the training. Colours in every group video:
# 0 파랑 = the clip's base policy, 1 초록 = old formula, 3 빨강 = new formula,
# 4 보라 = new formula with style weight 0.4 (kick); the final zombie run is filmed by run_arm.sh.
set -uo pipefail
D=$(dirname "$0")
FILM=experiments/style_walk/film.py
step() { echo "=== $(date +%H:%M:%S) $*"; }
group() {  # name, variants, colours
    step "group $1 ($2)"
    "$FILM" "$D" --variants "$2" --colors "$3" --name "group_$1" || echo "FAILED group_$1"
}
quality() {  # clip, variants
    step "quality $1"
    experiments/style_walk/quality_eval.py "$D" --variants "$2" || echo "FAILED quality $1"
    mkdir -p "$D/quality_$1" && cp "$D"/quality/* "$D/quality_$1/" 2>/dev/null
}
group walk_tired base,o_walk_tired,n_walk_tired 0,1,3
group walk_zombie base,o_walk_zombie,n_walk_zombie 0,1,3
group walk_sneak base,o_walk_sneak,n_walk_sneak 0,1,3
quality walk base,o_walk_tired,n_walk_tired,o_walk_zombie,n_walk_zombie,o_walk_sneak,n_walk_sneak
group run_tired base_run,o_run_B1,n_run_B1 0,1,3
group run_zombie base_run,o_run_B2,n_run_B2 0,1,3
quality run base_run,o_run_B1,n_run_B1,o_run_B2,n_run_B2,n2_run_B2
group jump_head base_jump,o_jump_B3,n_jump_B3 0,1,3
group jump_low base_jump,o_jump_B6,n_jump_B6 0,1,3
group jump_arms base_jump,o_jump_arms,n2_jump_A4 0,1,3
quality jump base_jump,o_jump_B3,n_jump_B3,o_jump_B6,n_jump_B6,o_jump_arms,n2_jump_A4
group kick_back base_kick,o_kick_B5,n_kick_B5,n_kick_B5_w4 0,1,3,4
quality kick base_kick,o_kick_B5,n_kick_B5,n_kick_B5_w4
group spin_tired base_spinkick,n_spin_tired 0,3
quality spinkick base_spinkick,n_spin_tired
rm -rf "$D/quality"
for key in n_walk_tired n_walk_zombie n_walk_sneak n_run_B1 n_jump_B3 n_jump_B6 n2_jump_A4 n_kick_B5 n_spin_tired; do
    [ -f "$D/$key/train/model.pt" ] || continue
    step "solo_$key"
    "$FILM" "$D" --variants "$key" --view quarter --name "solo_$key" || echo "FAILED solo_$key"
done
step "done"
