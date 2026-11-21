#!/usr/bin/env bash
# Final batch of the general-formula comparison (2026-11-03, results before 01:00): the remaining policies with the
# final formula (swing_unit + pose_unit + style w 0.2), the decisive checks first, then film_all.sh.
cd /home/jong/TexttoMotion
E=experiments/style_walk/20261101_225050_general_formula
R="./experiments/style_walk/run_style_walk.py --resume $E"
$R --iters 1500 --only n2_run_B2 >> $E/driver_final.log 2>&1
$R --iters 2000 --only n_walk_zombie >> $E/driver_final.log 2>&1
$R --iters 1500 --only n_run_B1,n_jump_B6,n_spin_tired,n2_jump_A4 >> $E/driver_final.log 2>&1
$R --iters 2000 --only n_walk_tired >> $E/driver_final.log 2>&1
$R --iters 1500 --only n_kick_B5_w4 >> $E/driver_final.log 2>&1
$R --iters 2000 --only n_walk_sneak >> $E/driver_final.log 2>&1
$E/film_all.sh > $E/film_driver.log 2>&1
