#!/bin/bash
# Batch B of 2026-11-16, after batch A: action chains through the pipeline (gpt-5.6-sol prompt-v12 answers to set 10:
# C2 run then jump, C3 walk then a front kick, C5 walk then a turning kick; plain DeepMimic on the joined clip) and
# both arms overhead in a V (shoulder_abduction 160 through the sideways hinge, hand-set); then the final runs.
cd /home/jong/TexttoMotion
LOG=experiments/style_walk/queue_20261116_b.log
until [ -f experiments/style_walk/queue_20261116_a.done ]; do sleep 60; done
EXP=$(./experiments/style_walk/make_llm_experiment.py experiments/style_llm/20261112_213225_v12_set10_gpt-5.6-sol C2,C3,C5 \
      --prefix s12 --name sol_v12_chains_trained)
E2=experiments/style_walk/20261112_213505_overhead_look
echo "$(date +%H:%M) training $EXP and arms_up_v" >> $LOG
./experiments/style_walk/run_style_walk.py --resume $E2 --iters 2000 --only arms_up_v > $E2/driver_b.log 2>&1
echo "$(date +%H:%M) arms_up_v trained" >> $LOG
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only s12_C2,s12_C3,s12_C5 > $EXP/driver.log 2>&1
echo "$(date +%H:%M) recording" >> $LOG
./experiments/style_eval/record_policies.py $EXP/s12_C2 $EXP/s12_C3 $EXP/s12_C5 $E2/arms_up_v > $EXP/record.log 2>&1
./experiments/chain/chain_check.py --trained $EXP > $EXP/chain_check.log 2>&1
for key in s12_C2 s12_C3 s12_C5; do
  ./experiments/style_walk/film.py $EXP --variants $key > $EXP/film_$key.log 2>&1
  ./experiments/style_walk/film.py $EXP --variants $key --view front > $EXP/film_front_$key.log 2>&1
done
./experiments/style_walk/film.py $E2 --variants arms_up_v,look_right,weave30,base > $E2/film_all.log 2>&1
./experiments/style_walk/film.py $E2 --variants arms_up_v,look_right,weave30,base --view front > $E2/film_all_front.log 2>&1
echo done > $EXP/run.done
echo "$(date +%H:%M) done" >> $LOG
echo done > experiments/style_walk/queue_20261116_b.done
bash experiments/style_walk/final_runs.sh $(cat experiments/style_walk/final_prompt.txt 2>/dev/null || echo v13)
