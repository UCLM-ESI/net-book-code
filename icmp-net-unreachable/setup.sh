#!/bin/bash

# Crear el namespace del router
ip netns add r1

# Crear la interfaz veth
ip link add veth-host type veth peer name veth-r1
ip link set veth-r1 netns r1

# Asignar IPs
ip addr add 192.168.200.100/24 dev veth-host
ip netns exec r1 ip addr add 192.168.200.1/24 dev veth-r1

# Activar interfaces
ip link set veth-host up
ip netns exec r1 ip link set veth-r1 up
ip netns exec r1 ip link set lo up

# Activar reenvío de paquetes en el router (por si acaso)
ip netns exec r1 sysctl -w net.ipv4.ip_forward=1

# Añadir ruta en el anfitrión hacia una red que no existe
ip route add 10.10.0.0/16 via 192.168.200.1

# Comprobar error "Network is unreachable"
ping -c 1 10.10.1.1
