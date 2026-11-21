#!/bin/bash
# Final evaluation runs (2026-11-16): the frozen pipeline (gpt-5.6-terra, prompt given as $1, e.g. v13) on the sets
# written before any run: 8 (numbers), 7 (styles, held out from prompt development), 9 (one-sided), 10 (chains, toes).
# For every set: the LLM answers (API, cached), an experiment folder of all accepted answers, 2000 iterations each,
# recording (4 characters x 30 s), the set's measurements, and films from the side and the front. Sets run one after
# another; a set whose answers cannot be fetched yet (daily request limit) is retried after the others.
# Usage: nohup bash experiments/style_walk/final_runs.sh v13 > /dev/null 2>&1 &
# Restarting it after a stop goes on from where it stopped (finished sets and policies are kept).
# SETS="10 7 9" bash experiments/style_walk/final_runs.sh v14 runs the sets in that order (default 8 7 9 10).
cd /home/jong/TexttoMotion
PROMPT=${1:-v13}
MODEL=gpt-5.6-terra
LOG=experiments/style_walk/final_runs.log
PY=/home/jong/isaaclab/.venv/bin/python

answers() {  # $1 = set; prints the run folder of the answers (generates them if missing)
  local run
  run=$(ls -d experiments/style_llm/*_${PROMPT}_set$1_$MODEL 2>/dev/null | tail -1)
  if [ -z "$run" ] || [ ! -f "$run/results.json" ]; then
    [ -n "$run" ] && rmdir "$run" 2>/dev/null  # an empty folder left by a run stopped at the request limit
    $PY experiments/style_llm/style_parser.py --test $1 --prompt $PROMPT --model api:$MODEL \
        >> experiments/style_walk/final_runs_api.log 2>&1
    run=$(ls -d experiments/style_llm/*_${PROMPT}_set$1_$MODEL 2>/dev/null | tail -1)
    if [ -z "$run" ] || [ ! -f "$run/results.json" ]; then
      [ -n "$run" ] && rm -rf "$run"
      return 1
    fi
  fi
  echo $run
}

train_set() {  # $1 = set, $2 = key prefix
  local run ids exp keys
  # A restart picks up where it stopped: a set whose folder has run.done is skipped, and an unfinished set goes on
  # in its own folder (run_style_walk.py --resume trains only the policies that are not completed).
  exp=$(ls -d experiments/style_walk/*_${2}_set$1_final 2>/dev/null | tail -1)
  if [ -n "$exp" ] && [ -f "$exp/run.done" ]; then
    echo "$(date +%H:%M) set $1: already done ($exp)" >> $LOG
    return 0
  fi
  run=$(answers $1) || { echo "$(date +%H:%M) set $1: answers not available yet" >> $LOG; return 1; }
  ids=$($PY -c "
import json, sys
rows = json.load(open('$run/results.json'))['results']
print(','.join(r['id'] for r in rows if 'params' in r and r.get('measure') != 'plain'))")
  [ -z "$exp" ] && exp=$(./experiments/style_walk/make_llm_experiment.py $run $ids --prefix $2 --name ${2}_set$1_final)
  keys=$(echo $ids | tr ',' '\n' | sed "s/^/$2_/" | paste -sd,)
  echo "$(date +%H:%M) set $1: training $exp ($keys)" >> $LOG
  ./experiments/style_walk/run_style_walk.py --resume $exp --iters 2000 --only $keys >> $exp/driver.log 2>&1
  echo "$(date +%H:%M) set $1: recording" >> $LOG
  ./experiments/style_eval/record_policies.py $(echo $keys | tr ',' '\n' | sed "s#^#$exp/#") > $exp/record.log 2>&1
  # the 100STYLE metric of every policy with a target (sets 7 and 9), and the set's own checks
  $PY -c "
import json
variants = json.load(open('$exp/variants.json'))
items = [{'label': v['key'], 'command': v['label'], 'rollout': '$(basename $exp)__' + v['key'],
          'base': '20261015_151030_walk_behaviors__base', 'target': v['source']['target']}
         for v in variants if v['key'] != 'base' and v.get('source', {}).get('target') and v.get('clip', 'walk') == 'walk']
json.dump({'title': 'final set $1 ($(basename $exp))', 'note': 'final runs, $MODEL prompt $PROMPT, 2000 iterations',
           'items': items}, open('experiments/style_eval/sets/final_set$1.json', 'w'), ensure_ascii=False, indent=1)
print(len(items))" > $exp/metric_items.log
  [ "$(cat $exp/metric_items.log)" != "0" ] && \
    ./experiments/style_eval/evaluate_policies.py experiments/style_eval/sets/final_set$1.json > $exp/evaluate.log 2>&1
  case $1 in
    8) ./experiments/t2m_compare/summarize.py ours $exp > $exp/summarize.log 2>&1
       ./experiments/t2m_compare/compare_set8.py $(basename $exp) > $exp/compare_set8.log 2>&1 ;;
    9) ./experiments/style_eval/side_check.py --trained $exp > $exp/side_check.log 2>&1 ;;
    10) ./experiments/chain/chain_check.py --trained $exp > $exp/chain_check.log 2>&1
        ./experiments/style_eval/side_check.py --trained $exp > $exp/side_check.log 2>&1 ;;
  esac
  # one film per reference clip (film.py loads one clip per simulation): walks six at a time with the plain walk,
  # every chain alone
  for group in $($PY -c "
import json
variants = {v['key']: v for v in json.load(open('$exp/variants.json'))}
keys = '$keys'.split(',')
walks = [k for k in keys if variants[k].get('clip', 'walk') == 'walk']
groups = [','.join(walks[i:i + 6] + ['base']) for i in range(0, len(walks), 6)]
groups += [k for k in keys if variants[k].get('clip', 'walk') != 'walk']
print(' '.join(groups))"); do
    name=$(echo $group | cut -d, -f1)
    ./experiments/style_walk/film.py $exp --variants $group --name $name > $exp/film_$name.log 2>&1
    ./experiments/style_walk/film.py $exp --variants $group --view front --name $name > $exp/film_front_$name.log 2>&1
  done
  echo done > $exp/run.done
  echo "$(date +%H:%M) set $1: done" >> $LOG
}

# First the weave check, whose training crashed in batch A (fixed in 52e70bf): retrain, record, film with the other checks.
E2=experiments/style_walk/20261112_213505_overhead_look
if [ ! -f $E2/weave30/train/model.pt ]; then
  echo "$(date +%H:%M) weave30: training" >> $LOG
  ./experiments/style_walk/run_style_walk.py --resume $E2 --iters 2000 --only weave30 > $E2/driver_weave.log 2>&1
  ./experiments/style_eval/record_policies.py $E2/weave30 > $E2/record_weave.log 2>&1
  ./experiments/style_walk/film.py $E2 --variants arms_up_v,look_right,weave30,base > $E2/film_all.log 2>&1
  ./experiments/style_walk/film.py $E2 --variants arms_up_v,look_right,weave30,base --view front > $E2/film_all_front.log 2>&1
  echo "$(date +%H:%M) weave30: done" >> $LOG
fi

pending=""
for set in ${SETS:-8 7 9 10}; do
  train_set $set f${set} || pending="$pending $set"
done
for set in $pending; do  # sets that waited for the daily request limit
  until train_set $set f${set}; do sleep 1800; done
done
echo "$(date +%H:%M) all final sets done" >> $LOG
