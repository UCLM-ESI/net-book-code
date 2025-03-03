#!/bin/bash

# Eliminar rutas
for ns in R01 R12 R23 Server; do
    ip netns exec $ns ip route flush table main
done

# Desactivar interfaces
ip link set Host.0 down
ip netns exec R01 ip link set R01.0 down
ip netns exec R01 ip link set R01.1 down
ip netns exec R12 ip link set R12.1 down
ip netns exec R12 ip link set R12.2 down
ip netns exec R23 ip link set R23.2 down
ip netns exec R23 ip link set R23.3 down
ip netns exec Server ip link set Server.3 down

# Eliminar interfaces
for iface in Host.0 R01.0 R01.1 R12.1 R12.2 R23.2 R23.3 Server.3; do
    sudo ip link delete $iface
done

# Eliminar namespaces
for ns in R01 R12 R23 Server; do
    sudo ip netns del $ns
done
