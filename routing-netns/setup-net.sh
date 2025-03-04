#!/bin/bash


set -x

# create namespaces
for ns in R01 R12 R23 Server; do
    ip netns add $ns
done

# create virtual ifaces
ip link add R01.e0 type veth peer name Host.e0
ip link add R01.e1 type veth peer name R12.e1
ip link add R12.e2 type veth peer name R23.e2
ip link add R23.e3 type veth peer name Server.e3

# assign ifaces to namespaces
ip link set R01.e0 netns R01
ip link set R01.e1 netns R01
ip link set R12.e1 netns R12
ip link set R12.e2 netns R12
ip link set R23.e2 netns R23
ip link set R23.e3 netns R23
ip link set Server.e3 netns Server

# enable interfaces
ip link set Host.e0 up
ip netns exec R01 ip link set R01.e0 up
ip netns exec R01 ip link set R01.e1 up
ip netns exec R12 ip link set R12.e1 up
ip netns exec R12 ip link set R12.e2 up
ip netns exec R23 ip link set R23.e2 up
ip netns exec R23 ip link set R23.e3 up
ip netns exec Server ip link set Server.e3 up

# assing IP addresses
ip addr add 10.0.0.1/24 dev Host.e0

ip netns exec R01 ip addr add 10.0.0.2/24 dev R01.e0
ip netns exec R01 ip addr add 10.0.1.1/24 dev R01.e1

ip netns exec R12 ip addr add 10.0.1.2/24 dev R12.e1
ip netns exec R12 ip addr add 10.0.2.1/24 dev R12.e2

ip netns exec R23 ip addr add 10.0.2.2/24 dev R23.e2
ip netns exec R23 ip addr add 10.0.3.1/24 dev R23.e3

ip netns exec Server ip addr add 10.0.3.2/24 dev Server.e3

# enable forwarding
for ns in R01 R12 R23; do
    ip netns exec $ns sysctl -w net.ipv4.ip_forward=1
done

# Host local gw
ip route add 10.0.0.0/16 via 10.0.0.2 dev Host.e0

# Server default router
ip netns exec Server ip route add default via 10.0.3.1 dev Server.e3
