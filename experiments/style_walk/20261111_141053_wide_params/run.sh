#!/bin/bash
# After the baseline batch: local LLM answers on set 7 (training-free scores), then the three strong values of the
# widened ranges (train, record, score, film). 2026-11-11.
cd /home/jong/TexttoMotion
EXP=experiments/style_walk/20261111_141053_wide_params
while [ ! -f experiments/style_walk/20261111_140324_v6_set6_trained/run.done ]; do sleep 30; done
PY=/home/jong/isaaclab/.venv/bin/python
$PY experiments/style_llm/style_parser.py --test 7 --prompt v6 --offline > $EXP/set7_4b_v6.log 2>&1
$PY experiments/style_llm/style_parser.py --test 7 --prompt v8 --model 8b-nf4 --batch-size 5 --offline > $EXP/set7_8b_v8.log 2>&1
for run in $(ls -d experiments/style_llm/*_set7* 2>/dev/null); do
  [ -f $run/style_metric.md ] || ./experiments/style_eval/score_generation.py $run >> $EXP/set7_score.log 2>&1
done
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only w_armsback,w_toein,w_together,w_bounce > $EXP/driver.log 2>&1
./experiments/style_eval/record_policies.py $EXP/w_armsback $EXP/w_toein $EXP/w_together $EXP/w_bounce > $EXP/record.log 2>&1
./experiments/style_eval/evaluate_policies.py experiments/style_eval/sets/wide_params.json > $EXP/evaluate.log 2>&1
./experiments/style_walk/film.py $EXP --variants w_armsback,w_toein,w_together,w_bounce,base > $EXP/film.log 2>&1
./experiments/style_walk/film.py $EXP --variants w_armsback,w_toein,w_together,w_bounce,base --view front > $EXP/film_front.log 2>&1
echo done > $EXP/run.done
