#!/bin/bash

for ns in R1 R2 R3 Client Server; do
    sudo ip netns del $ns
done
