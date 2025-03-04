#!/bin/bash -

for router in r01 r12 r23; do
    docker compose exec $router /usr/lib/frr/ripd -f /etc/frr/ripd.conf -d
done
