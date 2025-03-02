#!/bin/bash

#         0.0/24           1.0/24           2.0/24           3.0/24
# host ------------ R01 ------------ R12 ------------ R23 ------------ Server
#  0.1           0.2 | 1.1        1.2 | 2.1        2.2 | 3.1          s 3.2


set -x

# Crear namespaces
for ns in R01 R12 R23 Server; do
    ip netns add $ns
done

# Crear enlaces virtuales
ip link add R01.0 type veth peer name Host.0
ip link add R01.1 type veth peer name R12.1
ip link add R12.2 type veth peer name R23.2
ip link add R23.3 type veth peer name Server.3

# Asignar interfaces a los namespaces
ip link set R01.0 netns R01
ip link set R01.1 netns R01
ip link set R12.1 netns R12
ip link set R12.2 netns R12
ip link set R23.2 netns R23
ip link set R23.3 netns R23
ip link set Server.3 netns Server

# Activar interfaces
ip link set Host.0 up
ip netns exec R01 ip link set R01.0 up
ip netns exec R01 ip link set R01.1 up
ip netns exec R12 ip link set R12.1 up
ip netns exec R12 ip link set R12.2 up
ip netns exec R23 ip link set R23.2 up
ip netns exec R23 ip link set R23.3 up
ip netns exec Server ip link set Server.3 up

# Asignar IPs
ip addr add 10.0.0.1/24 dev Host.0

ip netns exec R01 ip addr add 10.0.0.2/24 dev R01.0
ip netns exec R01 ip addr add 10.0.1.1/24 dev R01.1

ip netns exec R12 ip addr add 10.0.1.2/24 dev R12.1
ip netns exec R12 ip addr add 10.0.2.1/24 dev R12.2

ip netns exec R23 ip addr add 10.0.2.2/24 dev R23.2
ip netns exec R23 ip addr add 10.0.3.1/24 dev R23.3

ip netns exec Server ip addr add 10.0.3.2/24 dev Server.3

# Habilitar reenvío en los routers
for ns in R01 R12 R23; do
    ip netns exec $ns sysctl -w net.ipv4.ip_forward=1
done

# Rutas
ip route add 10.0.0.0/16 via 10.0.0.2 dev Host.0
ip netns exec R01 ip route add default via 10.0.1.2 dev R01.1
ip netns exec R12 ip route add 10.0.0.0/24 via 10.0.1.1 dev R12.1
ip netns exec R12 ip route add 10.0.3.0/24 via 10.0.2.2 dev R12.2
ip netns exec R23 ip route add default via 10.0.2.1 dev R23.2
ip netns exec Server ip route add default via 10.0.3.1 dev Server.3
