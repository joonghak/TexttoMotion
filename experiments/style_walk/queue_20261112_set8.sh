#!/bin/bash
# Set 8 (numbers stated in the command) through our pipeline: the gpt-5.6-luna v10 answers trained 2000 iterations
# with the current formula, recorded, and measured like the T2M baselines (experiments/t2m_compare). 2026-11-12.
cd /home/jong/TexttoMotion
LOG=experiments/style_walk/queue_20261112_set8.log
until ls -d experiments/style_llm/*_v10_set8_gpt-5.6-luna >/dev/null 2>&1 && \
      [ -f "$(ls -d experiments/style_llm/*_v10_set8_gpt-5.6-luna | head -1)/results.json" ]; do sleep 60; done
RUN=$(ls -d experiments/style_llm/*_v10_set8_gpt-5.6-luna | head -1)
while pgrep -f "style_parser.py --test" >/dev/null; do sleep 60; done   # the local 4B v10 runs hold the GPU
echo "$(date +%H:%M) answers: $RUN" >> $LOG
EXP=$(./experiments/style_walk/make_llm_experiment.py $RUN Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13 --prefix l10 --name luna_v10_set8_trained)
echo "$(date +%H:%M) training $EXP" >> $LOG
KEYS=l10_Q1,l10_Q2,l10_Q3,l10_Q4,l10_Q5,l10_Q6,l10_Q7,l10_Q8,l10_Q9,l10_Q10,l10_Q11,l10_Q12,l10_Q13
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only $KEYS > $EXP/driver.log 2>&1
echo "$(date +%H:%M) recording" >> $LOG
./experiments/style_eval/record_policies.py $(echo $KEYS | tr ',' '\n' | sed "s#^#$EXP/#") > $EXP/record.log 2>&1
./experiments/style_walk/film.py $EXP --variants l10_Q1,l10_Q2,l10_Q3,l10_Q4,l10_Q9,l10_Q10,l10_Q11,base > $EXP/film.log 2>&1
./experiments/style_walk/film.py $EXP --variants l10_Q11,l10_Q12,l10_Q13,base --view front > $EXP/film_front.log 2>&1
echo done > $EXP/run.done
echo "$(date +%H:%M) done" >> $LOG
