#!/bin/bash -

for router in r1 r2 r3; do
    docker exec $router /usr/lib/frr/pimd -d -f /etc/frr/pimd.conf
done


for router in r1 r2 r3; do
    docker exec $router sysctl -w net.ipv4.conf.all.mc_forwarding=1
done
