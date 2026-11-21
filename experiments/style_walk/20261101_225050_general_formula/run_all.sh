#!/usr/bin/env bash
# Training queue of the general-formula comparison (2026-11-01): the transfer cases first, the walk checks last.
cd /home/jong/TexttoMotion
E=experiments/style_walk/20261101_225050_general_formula
./experiments/style_walk/run_style_walk.py --resume $E --iters 1500 --est-min 24 --only n_kick_B5,n_jump_B3,n_run_B2,n_kick_B5_w4,n_run_B1,n_jump_B6,n_spin_tired > $E/driver_1500.log 2>&1
./experiments/style_walk/run_style_walk.py --resume $E --iters 2000 --est-min 30 --only n_walk_tired,n_walk_zombie,n_walk_sneak > $E/driver_2000.log 2>&1
$E/film_all.sh > $E/film_driver.log 2>&1
