#!/bin/bash

tmux -f .tmux.conf new-session -d -s session
tmux -f .tmux.conf split-window -h
tmux -f .tmux.conf send-keys -t session:0.0 "sleep 2; ping -s700 10.0.1.3" C-m
tmux -f .tmux.conf send-keys -t session:0.1 "docker exec server tshark -f icmp" C-m
tmux -f .tmux.conf attach-session -t session
