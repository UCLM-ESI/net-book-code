#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Try with sudo."
    exit 1
fi

flush_ips() {
    local bridge_id=br-$1
    echo $bridge_id

    ip link set dev $bridge_id down
    ip addr flush dev $bridge_id
    ip -6 addr flush dev $bridge_id
    ip link set dev $bridge_id up
}

echo Removing bridge addresses...

for bridge in $(docker network ls --filter "driver=bridge" | grep "$(basename $(pwd))" | grep -v N0 | awk '{print $1}'); do
    flush_ips $bridge
done

echo Set lab default route...

if ! ip route show | grep -q '10.0.0.0/16 via 10.0.0.3'; then
    sudo ip route add 10.0.0.0/16 via 10.0.0.3
fi
