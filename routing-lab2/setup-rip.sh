#!/bin/bash -

for router in r1 r2 r3; do
    docker compose exec $router /usr/lib/frr/ripd -f /etc/frr/ripd.conf -d
done
