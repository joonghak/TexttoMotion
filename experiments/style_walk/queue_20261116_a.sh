#!/bin/bash
# Batch A of 2026-11-16 (the checks stopped on 11-12): terra's set-9 answer S8 (heavy bag on the left shoulder: lean,
# head tilt, left arm), foot_pitch 25 (tiptoe), head_yaw 50 (look right) and weave 0.3 (weaving path), 2000 iterations
# each (about 2 h 15 min with recording, the one-sided check and filming from the side and the front).
cd /home/jong/TexttoMotion
LOG=experiments/style_walk/queue_20261116_a.log
E1=experiments/style_walk/20261112_221819_terra_v11_set9_trained
E2=experiments/style_walk/20261112_213505_overhead_look
echo "$(date +%H:%M) training" >> $LOG
./experiments/style_walk/run_style_walk.py --resume $E1 --iters 2000 --only t11_S8,toe25 > $E1/driver_b.log 2>&1
./experiments/style_walk/run_style_walk.py --resume $E2 --iters 2000 --only look_right,weave30 > $E2/driver.log 2>&1
echo "$(date +%H:%M) recording" >> $LOG
./experiments/style_eval/record_policies.py $E1/t11_S8 $E1/toe25 $E2/look_right $E2/weave30 > $E1/record_b.log 2>&1
./experiments/style_eval/side_check.py --trained $E1 > $E1/side_check.log 2>&1
./experiments/style_eval/side_check.py --trained $E2 > $E2/side_check.log 2>&1
./experiments/style_walk/film.py $E1 --variants t11_S1,t11_S2,t11_S8,toe25,base > $E1/film.log 2>&1
./experiments/style_walk/film.py $E1 --variants t11_S1,t11_S2,t11_S8,toe25,base --view front > $E1/film_front.log 2>&1
./experiments/style_walk/film.py $E2 --variants look_right,weave30,base > $E2/film.log 2>&1
./experiments/style_walk/film.py $E2 --variants look_right,weave30,base --view front > $E2/film_front.log 2>&1
echo "$(date +%H:%M) done" >> $LOG
echo done > experiments/style_walk/queue_20261116_a.done
