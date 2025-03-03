#!/bin/bash

# remove routes
for ns in R01 R12 R23 Server; do
    ip netns exec $ns ip route flush table main
done

# disable ifaces
ip link set Host.e0 down
ip netns exec R01 ip link set R01.e0 down
ip netns exec R01 ip link set R01.e1 down
ip netns exec R12 ip link set R12.e1 down
ip netns exec R12 ip link set R12.e2 down
ip netns exec R23 ip link set R23.e2 down
ip netns exec R23 ip link set R23.e3 down
ip netns exec Server ip link set Server.e3 down

# remove ifaces
for iface in Host.e0 R01.e0 R01.e1 R12.e1 R12.e2 R23.e2 R23.e3 Server.e3; do
    sudo ip link delete $iface
done

# remove namespaces
for ns in R01 R12 R23 Server; do
    sudo ip netns del $ns
done

killall zebra
killall ripd
