#!/bin/bash -

for router in r1 r2 r3; do
    docker exec $router /usr/lib/frr/frrinit.sh start
done
