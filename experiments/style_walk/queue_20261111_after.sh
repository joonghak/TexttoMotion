#!/bin/bash
# After queue_20261111.sh: Qwen3-4B with prompt v10 on sets 6 and 7 (same prompt as the API runs), scored, to
# separate the effect of the model from that of the prompt and the new parameters.
cd /home/jong/TexttoMotion
PY=/home/jong/isaaclab/.venv/bin/python
until grep -q "all done" experiments/style_walk/queue_20261111.log 2>/dev/null; do sleep 60; done
echo "$(date +%H:%M) 4B v10" >> experiments/style_walk/queue_20261111.log
for set in 6 7; do
  $PY experiments/style_llm/style_parser.py --test $set --prompt v10 --offline >> experiments/style_llm/logs/4b_v10.log 2>&1
done
for run in $(ls -d experiments/style_llm/*_v10_set6 experiments/style_llm/*_v10_set7 2>/dev/null); do
  [ -f $run/results.json ] && [ ! -f $run/style_metric.md ] && ./experiments/style_eval/score_generation.py $run >> experiments/style_llm/logs/4b_v10.log 2>&1
done
echo "$(date +%H:%M) 4B v10 done" >> experiments/style_walk/queue_20261111.log
