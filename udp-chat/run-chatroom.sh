#!/bin/bash

(
    unalias -a
    unset -f $(compgen -A function)
    export PS1='$ '

    tmux -f .tmux.conf new-session -d -s session
    tmux -f .tmux.conf split-window -h -t session:0

    tmux -f .tmux.conf split-window -v -t session:0.1
    tmux -f .tmux.conf split-window -v -t session:0.2

    tmux -f .tmux.conf send-keys -t session:0.0 "./chatroom-broker.py& disown; clear" C-m
    tmux -f .tmux.conf send-keys -t session:0.1 "./chatroom-member.py & disown; clear" C-m
    tmux -f .tmux.conf send-keys -t session:0.2 "./chatroom-member.py & disown; clear" C-m
    tmux -f .tmux.conf send-keys -t session:0.3 "./chatroom-member.py & disown; clear" C-m

    tmux -f .tmux.conf attach-session -t session
)
