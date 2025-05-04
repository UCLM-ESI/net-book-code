#!/bin/bash
shopt -s expand_aliases
alias tmux='tmux -f .tmux.conf'

tmux new-session -d -s session

tmux send-keys -t session:0.0 'clear; echo "==== Puedes cerrar esta ventana con Ctrl-b x ===="; bash' C-m

tmux split-window -h -t session:0.0
tmux split-window -v -t session:0.0

tmux send-keys -t session:0.0 "docker exec server1 iperf -c 239.1.1.1 -u -t 30" C-m
tmux send-keys -t session:0.1 "docker exec server2 iperf -s -u -B 239.1.1.1" C-m
tmux send-keys -t session:0.2 "docker exec r2 tshark -i eth2 -f 'ip dst 239.1.1.1'" C-m

tmux attach-session -t session
