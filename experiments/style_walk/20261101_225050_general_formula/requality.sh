#!/bin/bash
# Quality numbers again after quality_eval.py measures each policy against its own formula's targets
# (before: the first variant's swing unit and arm anchor for all). Policies and videos are unchanged.
set -uo pipefail
cd /home/jong/TexttoMotion
D=experiments/style_walk/20261101_225050_general_formula
quality() {  # clip, variants
    echo "=== $(date +%H:%M:%S) quality $1"
    experiments/style_walk/quality_eval.py "$D" --variants "$2" || echo "FAILED quality $1"
    mkdir -p "$D/quality_$1" && cp "$D"/quality/* "$D/quality_$1/" 2>/dev/null
}
quality run base_run,o_run_B1,n_run_B1,o_run_B2,n_run_B2,n2_run_B2,n3_run_B2
quality jump base_jump,o_jump_B3,n_jump_B3,o_jump_B6,n_jump_B6,o_jump_arms,n2_jump_A4
quality walk base,o_walk_tired,n_walk_tired,o_walk_zombie,n_walk_zombie,o_walk_sneak,n_walk_sneak
quality kick base_kick,o_kick_B5,n_kick_B5,n_kick_B5_w4
quality spinkick base_spinkick,n_spin_tired
rm -rf "$D/quality"
echo "=== $(date +%H:%M:%S) done"
