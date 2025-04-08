#!/bin/bash -

for router in r1 r2 r3; do
    docker exec $router /usr/lib/frr/eigrpd -f /etc/frr/eigrpd.conf -d
done
