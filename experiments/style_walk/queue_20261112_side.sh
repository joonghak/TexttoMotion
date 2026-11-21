#!/bin/bash
# One-sided values (prompt v11) and tiptoe (foot_pitch), 2026-11-12: gpt-5.6-terra's set-9 answers S1 (limp, right
# knee nearly straight), S2 (left hand raised), S8 (heavy bag on the left shoulder: lean, head tilt, left arm) and a
# hand-set foot_pitch 25 for walking on the toes, trained 2000 iterations after the set-8 batch, recorded, checked on
# the one-sided measures and filmed from the side and the front (about 2 h 10 min).
cd /home/jong/TexttoMotion
LOG=experiments/style_walk/queue_20261112_side.log
while [ ! -f experiments/style_walk/20261112_154003_luna_v10_set8_trained/run.done ]; do sleep 60; done
EXP=$(./experiments/style_walk/make_llm_experiment.py experiments/style_llm/20261112_211507_v11_set9_gpt-5.6-terra S1,S2,S8 \
      --prefix t11 --name terra_v11_set9_trained)
/home/jong/isaaclab/.venv/bin/python - "$EXP" <<'EOF'
import json, sys
from pathlib import Path
path = Path(sys.argv[1]) / "variants.json"
variants = json.loads(path.read_text())
variants.append({"key": "toe25", "label": "까치발 걸음을 노린 새 항 확인 (사람이 정한 값): 발끝 세우기 25°",
                 "scales": {"foot_pitch": 25}, "params": {"foot_pitch": 25}})
path.write_text(json.dumps(variants, ensure_ascii=False, indent=1))
EOF
echo "$(date +%H:%M) training $EXP" >> $LOG
KEYS=t11_S1,t11_S2,t11_S8,toe25
./experiments/style_walk/run_style_walk.py --resume $EXP --iters 2000 --only $KEYS > $EXP/driver.log 2>&1
echo "$(date +%H:%M) recording" >> $LOG
./experiments/style_eval/record_policies.py $EXP/t11_S1 $EXP/t11_S2 $EXP/t11_S8 $EXP/toe25 > $EXP/record.log 2>&1
./experiments/style_eval/side_check.py --trained $EXP > $EXP/side_check.log 2>&1
./experiments/style_walk/film.py $EXP --variants t11_S1,t11_S2,t11_S8,toe25,base > $EXP/film.log 2>&1
./experiments/style_walk/film.py $EXP --variants t11_S1,t11_S2,t11_S8,toe25,base --view front > $EXP/film_front.log 2>&1
echo done > $EXP/run.done
echo "$(date +%H:%M) done" >> $LOG
