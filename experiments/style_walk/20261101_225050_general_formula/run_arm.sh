#!/usr/bin/env bash
# Added 2026-11-03 16:45: the zombie run with the final arm anchor (walk arm pose in the heading frame, n3_run_B2),
# after run_final.sh (texttomotion-formula-final) has finished training and filming.
cd /home/jong/TexttoMotion
E=experiments/style_walk/20261101_225050_general_formula
while systemctl --user is-active --quiet texttomotion-formula-final; do sleep 60; done
./experiments/style_walk/run_style_walk.py --resume $E --iters 1500 --only n3_run_B2 >> $E/driver_final.log 2>&1
{
FILM=experiments/style_walk/film.py
echo "=== $(date +%H:%M:%S) group run_zombie_final"
"$FILM" $E --variants base_run,o_run_B2,n_run_B2,n3_run_B2 --colors 0,1,3,4 --name group_run_zombie_final
echo "=== $(date +%H:%M:%S) quality run"
experiments/style_walk/quality_eval.py $E --variants base_run,o_run_B1,n_run_B1,o_run_B2,n_run_B2,n2_run_B2,n3_run_B2 && \
    mkdir -p $E/quality_run && cp $E/quality/* $E/quality_run/
rm -rf $E/quality
echo "=== $(date +%H:%M:%S) solo_n3_run_B2"
"$FILM" $E --variants n3_run_B2 --view quarter --name solo_n3_run_B2
echo "=== $(date +%H:%M:%S) done"
} > $E/film_arm.log 2>&1
