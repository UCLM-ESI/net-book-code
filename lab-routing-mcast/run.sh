#!/bin/bash
shopt -s expand_aliases
alias tmux='tmux -f .tmux.conf'

tmux new-session -d -s session
tmux send-keys 'clear; echo "==== Puedes cerrar esta ventana con Ctrl-b x ===="; bash' C-m
tmux split-window -h
tmux send-keys -t session:0.0 "docker exec server1 iperf -c 239.1.1.1 -u -t 30" C-m
tmux send-keys -t session:0.1 "docker exec server2 iperf -s -u -B 239.1.1.1" C-m
# tmux send-keys -t session:0.1 "socat -v UDP-RECV:5000,ip-add-membership=239.1.1.1:10.0.0.1 -" C-m
tmux attach-session -t session
