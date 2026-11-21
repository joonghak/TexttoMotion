#!/usr/bin/env bash
# Second step (added 2026-11-02 00:25 after the zombie run's front view): arm offsets measured from the walk's arm pose
# (pose_unit). Waits for the first queue (run_all.sh) to finish, then trains, films and measures the two arm cases.
cd /home/jong/TexttoMotion
E=experiments/style_walk/20261101_225050_general_formula
while systemctl --user is-active --quiet texttomotion-general-formula; do sleep 60; done
./experiments/style_walk/run_style_walk.py --resume $E --iters 1500 --est-min 24 --only n2_run_B2,n2_jump_A4 > $E/driver_extra.log 2>&1
{
FILM=experiments/style_walk/film.py
echo "=== $(date +%H:%M:%S) group run_zombie_arms"
"$FILM" $E --variants base_run,o_run_B2,n_run_B2,n2_run_B2 --colors 0,1,3,4 --name group_run_zombie_arms
echo "=== $(date +%H:%M:%S) group jump_arms"
"$FILM" $E --variants base_jump,o_jump_arms,n2_jump_A4 --colors 0,1,4 --name group_jump_arms
echo "=== $(date +%H:%M:%S) quality run"
experiments/style_walk/quality_eval.py $E --variants base_run,o_run_B1,n_run_B1,o_run_B2,n_run_B2,n2_run_B2 && \
    mkdir -p $E/quality_run && cp $E/quality/* $E/quality_run/
echo "=== $(date +%H:%M:%S) quality jump"
experiments/style_walk/quality_eval.py $E --variants base_jump,o_jump_B3,n_jump_B3,o_jump_B6,n_jump_B6,o_jump_arms,n2_jump_A4 && \
    mkdir -p $E/quality_jump && cp $E/quality/* $E/quality_jump/
rm -rf $E/quality
for key in n2_run_B2 n2_jump_A4; do
    echo "=== $(date +%H:%M:%S) solo_$key"
    "$FILM" $E --variants $key --view quarter --name solo_$key
done
echo "=== $(date +%H:%M:%S) done"
} > $E/film_extra.log 2>&1
