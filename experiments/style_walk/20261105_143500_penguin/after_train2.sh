#!/usr/bin/env bash
cd /home/jong/TexttoMotion
while systemctl --user is-active --quiet llm_chain; do sleep 20; done
echo "=== train start $(date +%H:%M)"
./experiments/style_walk/run_style_walk.py --resume experiments/style_walk/20261105_143500_penguin --iters 2000 >> experiments/style_walk/20261105_143500_penguin/driver.log 2>&1 || echo FAILED train
echo "=== train done $(date +%H:%M)"
./experiments/style_eval/record_policies.py experiments/style_walk/20261105_143500_penguin/pen_d experiments/style_walk/20261105_143500_penguin/pen_e --seconds 30 --replicas 4 || echo FAILED record
./experiments/style_walk/film.py experiments/style_walk/20261105_143500_penguin --variants base,pen_c,pen_d,pen_e --colors 0,4,3,1 --name group_penguin2 || echo FAILED film side
./experiments/style_walk/film.py experiments/style_walk/20261105_143500_penguin --variants base,pen_c,pen_d,pen_e --colors 0,4,3,1 --view front --name penguin2 || echo FAILED film front
echo "=== all done $(date +%H:%M)"
