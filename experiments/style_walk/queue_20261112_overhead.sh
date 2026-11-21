#!/bin/bash
# Three mechanism checks after the chain batch (2026-11-12): arms overhead in a V through the shoulders' sideways hinge
# (the forward hinge stops at 90 degrees, the sideways one reaches 110 above horizontal), and the head turned 50
# degrees (head_yaw of prompt v11, untrained), and the path weaving 0.3 m sideways (weave). Hand-set values; trained, recorded, filmed from the side and the front.
cd /home/jong/TexttoMotion
until ls experiments/style_walk/*_sol_v12_chains_trained/run.done >/dev/null 2>&1; do sleep 60; done
EXP=experiments/style_walk/20261112_213505_overhead_look
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only arms_up_v,look_right,weave30 > $EXP/driver.log 2>&1
./experiments/style_eval/record_policies.py $EXP/arms_up_v $EXP/look_right $EXP/weave30 > $EXP/record.log 2>&1
./experiments/style_walk/film.py $EXP --variants arms_up_v,look_right,weave30,base > $EXP/film.log 2>&1
./experiments/style_walk/film.py $EXP --variants arms_up_v,look_right,weave30,base --view front > $EXP/film_front.log 2>&1
echo done > $EXP/run.done
