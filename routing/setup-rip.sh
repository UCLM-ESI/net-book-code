ip netns exec R01 ripd -f ripd-R01.conf -z /var/run/frr/R01_ripd.vty -d
ip netns exec R12 ripd -f ripd-R12.conf -z /var/run/frr/R12_ripd.vty -d
ip netns exec R23 ripd -f ripd-R23.conf -z /var/run/frr/R23_ripd.vty -d
