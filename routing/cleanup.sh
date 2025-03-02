#!/bin/bash

# Eliminar las rutas de los routers
ip netns exec R01 ip route flush table main
ip netns exec R12 ip route flush table main
ip netns exec R23 ip route flush table main
ip netns exec Server ip route flush table main

# Desactivar las interfaces en cada namespace
ip link set Host.0 down
ip netns exec R01 ip link set R01.0 down
ip netns exec R01 ip link set R01.1 down
ip netns exec R12 ip link set R12.1 down
ip netns exec R12 ip link set R12.2 down
ip netns exec R23 ip link set R23.2 down
ip netns exec R23 ip link set R23.3 down
ip netns exec Server ip link set Server.3 down

# Eliminar las interfaces virtuales (veth pairs)
ip link delete Host.0
ip link delete R01.0
ip link delete R01.1
ip link delete R12.1
ip link delete R12.2
ip link delete R23.2
ip link delete R23.3
ip link delete Server.3

# Eliminar los network namespaces
for ns in R01 R12 R23 Server; do
    sudo ip netns del $ns
done
