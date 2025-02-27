#!/bin/bash

#       192.168.1.0/24       10.0.0.0/30       10.0.0.4/30       192.168.2.0/24
# Client ------------ R1 ---------------- R3 ---------------- R2 ------------ Server
#                     veth1        veth2  veth3        veth4  veth5

#!/bin/bash

# Crear network namespaces para los routers
for ns in R01 R12 R02; do
    ip netns add $ns
done

# Crear enlaces virtuales (veth pairs)
ip link add veth-R01 type veth peer name veth-R01-R12
ip link add veth-R01-R12 type veth peer name veth-R12
ip link add veth-R12-R02 type veth peer name veth-R02
ip link add veth-R02 type veth peer name veth-host

# Asignar interfaces a los namespaces correspondientes
ip link set veth-R01 netns R01
ip link set veth-R01-R12 netns R01
ip link set veth-R12 netns R12
ip link set veth-R12-R02 netns R12
ip link set veth-R02 netns R02


# Configuración de direcciones IP
# Red 1 (N1)
ip netns exec R01 ip addr add 192.168.1.1/24 dev veth-R01
ip netns exec R01 ip addr add 10.0.0.1/30 dev veth-R01-R12

# Red 2 (N2)
ip netns exec R12 ip addr add 10.0.0.2/30 dev veth-R01-R12
ip netns exec R12 ip addr add 10.0.0.5/30 dev veth-R12-R02

# Servidor en la Red 2
ip netns exec R02 ip addr add 192.168.2.1/24 dev veth-R02
ip netns exec R02 ip addr add 10.0.0.6/30 dev veth-R12-R02

# Configuración de las interfaces de red para el cliente y servidor (host)
ip addr add 192.168.1.100/24 dev veth-host   # Cliente (host)
ip addr add 192.168.2.100/24 dev veth-host   # Servidor (host)

# Activar interfaces en todos los namespaces
for ns in R01 R12 R02; do
    ip netns exec $ns ip link set lo up
    ip netns exec $ns ip link set veth-R01 up || true
    ip netns exec $ns ip link set veth-R01-R12 up || true
    ip netns exec $ns ip link set veth-R12 up || true
    ip netns exec $ns ip link set veth-R12-R02 up || true
    ip netns exec $ns ip link set veth-R02 up || true
done

# Habilitar encaminamiento IP en los routers
for ns in R01 R12 R02; do
    ip netns exec $ns sysctl -w net.ipv4.ip_forward=1
done

# Configuración de rutas estáticas
ip netns exec R01 ip route add 192.168.2.0/24 via 10.0.0.2
ip netns exec R12 ip route add 192.168.1.0/24 via 10.0.0.5
ip route add 192.168.1.0/24 via 192.168.2.1  # Desde el Cliente hacia el Servidor
ip route add 192.168.2.0/24 via 192.168.1.1  # Desde el Servidor hacia el Cliente
