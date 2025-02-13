#!/bin/bash

tmux -f .tmux.conf new-session -d -s session
tmux -f .tmux.conf split-window -h
tmux -f .tmux.conf send-keys -t session:0.0 './server.py 2000 | mplayer -msglevel all=-1 -' C-m
tmux -f .tmux.conf send-keys -t session:0.1 'sleep 2; ./client.py localhost 2000 < song.mp3' C-m
tmux -f .tmux.conf attach-session -t session
