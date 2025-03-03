#!/bin/bash

run_rip() {
    local NS="$1"
    ip netns exec $NS /usr/lib/frr/zebra -i /tmp/$NS-zebra.pid -d

    unshare -m bash <<EOF
        mount --bind rip/$NS-ripd.conf /etc/frr/ripd.conf
        ip netns exec $NS /usr/lib/frr/ripd -i /tmp/$NS-ripd.pid -d
        exit
EOF
}

systemctl stop frr
systemctl disable frr
touch /etc/frr/ripd.conf

for ns in R01 R12 R23; do
    run_rip $ns
done
