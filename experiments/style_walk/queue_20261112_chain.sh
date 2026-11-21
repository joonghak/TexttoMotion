#!/bin/bash
# Action chaining through the whole pipeline (2026-11-12): gpt-5.6-sol's prompt-v12 answers to set 10, C2 (run, then
# jump), C3 (walk, then a front kick) and C5 (walk, then a turning kick). Their chains were joined into reference clips
# by experiments/chain/compose_chain.py when the answers were parsed; each is trained 2000 iterations as plain DeepMimic
# on its chain (no style), after the one-sided batch, and filmed once from the start of the chain (side, front).
cd /home/jong/TexttoMotion
LOG=experiments/style_walk/queue_20261112_chain.log
until ls experiments/style_walk/*_terra_v11_set9_trained/run.done >/dev/null 2>&1; do sleep 60; done
EXP=$(./experiments/style_walk/make_llm_experiment.py experiments/style_llm/20261112_213225_v12_set10_gpt-5.6-sol C2,C3,C5 \
      --prefix s12 --name sol_v12_chains_trained)
echo "$(date +%H:%M) training $EXP" >> $LOG
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only s12_C2,s12_C3,s12_C5 > $EXP/driver.log 2>&1
echo "$(date +%H:%M) filming" >> $LOG
for key in s12_C2 s12_C3 s12_C5; do
  ./experiments/style_walk/film.py $EXP --variants $key > $EXP/film_$key.log 2>&1
  ./experiments/style_walk/film.py $EXP --variants $key --view front > $EXP/film_front_$key.log 2>&1
done
echo done > $EXP/run.done
echo "$(date +%H:%M) done" >> $LOG
