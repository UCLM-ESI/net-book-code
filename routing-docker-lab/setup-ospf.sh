#!/bin/bash -

for router in r01 r12 r23; do
    docker compose exec $router /usr/lib/frr/ospfd -f /etc/frr/ospfd.conf -d
done
