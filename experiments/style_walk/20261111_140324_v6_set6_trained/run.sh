#!/bin/bash
# Train the four 4B v6 answers, record and score them, film them (2026-11-11).
cd /home/jong/TexttoMotion
EXP=experiments/style_walk/20261111_140324_v6_set6_trained
while pgrep -f film_compare.py >/dev/null; do sleep 10; done
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only v6_N4,v6_N3,v6_P5,v6_M3 > $EXP/driver.log 2>&1
./experiments/style_eval/record_policies.py $EXP/v6_N4 $EXP/v6_N3 $EXP/v6_P5 $EXP/v6_M3 > $EXP/record.log 2>&1
./experiments/style_eval/evaluate_policies.py experiments/style_eval/sets/v6_set6_trained.json > $EXP/evaluate.log 2>&1
./experiments/style_walk/film.py $EXP --variants v6_N4,v6_N3,v6_P5,v6_M3,base > $EXP/film.log 2>&1
./experiments/style_walk/film.py $EXP --variants v6_N4,v6_N3,v6_P5,v6_M3,base --view front > $EXP/film_front.log 2>&1
echo done > $EXP/run.done
