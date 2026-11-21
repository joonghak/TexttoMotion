#!/bin/bash
# 2026-11-18: the six policies the human study still needs (set 10 C2 and C5, set 7 P3 to P6) are trained first, so the
# study videos (make_study_films.py, which needs only train/model.pt) can be made about 4.5 h after the start instead
# of about 12 h. Then the final queue goes on as before (final_runs.sh skips every policy already trained).
# Same training as final_runs.sh: run_style_walk.py --resume, 2000 iterations.
# Usage: setsid nohup bash experiments/style_walk/study_first.sh > /dev/null 2>&1 < /dev/null &
cd /home/jong/TexttoMotion
LOG=experiments/style_walk/final_runs.log
E10=experiments/style_walk/20261118_120930_f10_set10_final
E7=experiments/style_walk/20261116_232101_f7_set7_final
echo "$(date +%H:%M) study policies first: f10_C2, f10_C5, f7_P3 to f7_P6" >> $LOG
./experiments/style_walk/run_style_walk.py --resume $E10 --iters 2000 --only f10_C2,f10_C5 >> $E10/driver.log 2>&1
./experiments/style_walk/run_style_walk.py --resume $E7 --iters 2000 --only f7_P3,f7_P4,f7_P5,f7_P6 >> $E7/driver.log 2>&1
echo "$(date +%H:%M) study policies trained" >> $LOG
SETS="10 7 9" bash experiments/style_walk/final_runs.sh v14
