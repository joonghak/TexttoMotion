#!/bin/bash
# Queue of 2026-11-11 after the baseline batch (4B v6 answers): set-7 answers of the local models (training-free
# scores), the gpt-5.6-terra v10 answers trained, then the strong values of the widened ranges.
cd /home/jong/TexttoMotion
PY=/home/jong/isaaclab/.venv/bin/python
W=experiments/style_walk/20261111_141053_wide_params
T=experiments/style_walk/20261111_150859_terra_v10_set6_trained
while [ ! -f experiments/style_walk/20261111_140324_v6_set6_trained/run.done ]; do sleep 30; done
echo "$(date +%H:%M) set 7 local" >> experiments/style_walk/queue_20261111.log
$PY experiments/style_llm/style_parser.py --test 7 --prompt v6 --offline > $W/set7_4b_v6.log 2>&1
$PY experiments/style_llm/style_parser.py --test 7 --prompt v8 --model 8b-nf4 --batch-size 5 --offline > $W/set7_8b_v8.log 2>&1
for run in $(ls -d experiments/style_llm/*_set7* 2>/dev/null); do
  [ -f $run/results.json ] && [ ! -f $run/style_metric.md ] && ./experiments/style_eval/score_generation.py $run >> $W/set7_score.log 2>&1
done
echo "$(date +%H:%M) terra training" >> experiments/style_walk/queue_20261111.log
./experiments/style_walk/run_style_walk.py --resume $T --iters 2000 --only t10_N4,t10_N3,t10_P5,t10_M3,t10_N1,t10_N2 > $T/driver.log 2>&1
./experiments/style_eval/record_policies.py $T/t10_N4 $T/t10_N3 $T/t10_P5 $T/t10_M3 $T/t10_N1 $T/t10_N2 > $T/record.log 2>&1
./experiments/style_eval/evaluate_policies.py experiments/style_eval/sets/terra_v10_set6_trained.json > $T/evaluate.log 2>&1
./experiments/style_walk/film.py $T --variants t10_N4,t10_N3,t10_P5,t10_M3,t10_N1,t10_N2 > $T/film.log 2>&1
./experiments/style_walk/film.py $T --variants t10_N4,t10_N3,t10_P5,t10_M3,t10_N1,t10_N2 --view front > $T/film_front.log 2>&1
echo done > $T/run.done
echo "$(date +%H:%M) wide ranges" >> experiments/style_walk/queue_20261111.log
./experiments/style_walk/run_style_walk.py --resume $W --iters 2000 --only w_armsback,w_toein,w_together,w_bounce > $W/driver.log 2>&1
./experiments/style_eval/record_policies.py $W/w_armsback $W/w_toein $W/w_together $W/w_bounce > $W/record.log 2>&1
./experiments/style_eval/evaluate_policies.py experiments/style_eval/sets/wide_params.json > $W/evaluate.log 2>&1
./experiments/style_walk/film.py $W --variants w_armsback,w_toein,w_together,w_bounce,base > $W/film.log 2>&1
./experiments/style_walk/film.py $W --variants w_armsback,w_toein,w_together,w_bounce,base --view front > $W/film_front.log 2>&1
echo done > $W/run.done
echo "$(date +%H:%M) all done" >> experiments/style_walk/queue_20261111.log
