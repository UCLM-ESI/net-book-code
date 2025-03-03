ip netns exec R01 ip route add default via 10.0.1.2 dev R01.1
ip netns exec R12 ip route add 10.0.0.0/24 via 10.0.1.1 dev R12.1
ip netns exec R12 ip route add 10.0.3.0/24 via 10.0.2.2 dev R12.2
ip netns exec R23 ip route add default via 10.0.2.1 dev R23.2
ip netns exec Server ip route add default via 10.0.3.1 dev Server.3
