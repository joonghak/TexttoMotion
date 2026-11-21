#!/bin/bash
# The three text-to-motion models on sets 9 and 10 (one-sided walks, chains of actions, toes and heels), 2026-11-16,
# on the CPU while the GPU trains our policies; then their measurements (summarize.py).
cd /home/jong/TexttoMotion
PY=/home/jong/baselines/venv/bin/python
P=experiments/t2m_compare/prompts_910.json
O=experiments/t2m_compare/out
$PY experiments/t2m_compare/gen_momask.py $P $O/momask --repeats 3 --cpu > $O/gen_910_momask.log 2>&1
$PY experiments/t2m_compare/gen_t2mgpt.py $P $O/t2mgpt --repeats 3 --cpu > $O/gen_910_t2mgpt.log 2>&1
$PY experiments/t2m_compare/gen_mdm.py $P $O/mdm --repeats 3 --cpu > $O/gen_910_mdm.log 2>&1
echo done > $O/gen_910.done
