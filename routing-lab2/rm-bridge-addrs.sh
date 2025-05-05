#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Try with sudo."
    exit 1
fi

flush_ips() {
    local bridge_id=$1
    echo -n "$bridge_id "

    ip link set dev $bridge_id down
    ip addr flush dev $bridge_id
    ip -6 addr flush dev $bridge_id
    ip link set dev $bridge_id up
}

echo -n "-- Removing host bridge addresses: "

for bridge in N1 N2 N3; do
    flush_ips $bridge
done

echo "done"
