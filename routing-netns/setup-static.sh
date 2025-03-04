ip netns exec R01 ip route add default via 10.0.1.2 dev R01.e1
ip netns exec R12 ip route add 10.0.0.0/24 via 10.0.1.1 dev R12.e1
ip netns exec R12 ip route add 10.0.3.0/24 via 10.0.2.2 dev R12.e2
ip netns exec R23 ip route add default via 10.0.2.1 dev R23.e2
