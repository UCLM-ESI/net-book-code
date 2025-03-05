#!/bin/bash -

for router in r1 r2 r3; do
    docker compose exec $router /usr/lib/frr/ospfd -f /etc/frr/ospfd.conf -d
done
