#!/usr/bin/env bash
cd /home/jong/TexttoMotion
while systemctl --user is-active --quiet penguin_train; do sleep 20; done
echo "=== train done $(date +%H:%M)"
./experiments/style_eval/record_policies.py experiments/style_walk/20261105_143500_penguin/pen_a experiments/style_walk/20261105_143500_penguin/pen_b experiments/style_walk/20261105_143500_penguin/pen_c --seconds 30 --replicas 4 || echo FAILED record
./experiments/style_walk/film.py experiments/style_walk/20261105_143500_penguin --variants base,pen_a,pen_b,pen_c --colors 0,1,3,4 --name group_penguin || echo FAILED film side
./experiments/style_walk/film.py experiments/style_walk/20261105_143500_penguin --variants base,pen_a,pen_b,pen_c --colors 0,1,3,4 --view front --name penguin || echo FAILED film front
echo "=== all done $(date +%H:%M)"
