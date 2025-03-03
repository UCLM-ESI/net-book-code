

## Topology:

    All prefix are 10.0.

            0.0/24           1.0/24           2.0/24           3.0/24
    host ------------ R01 ------------ R12 ------------ R23 ------------ Server
       0.1         0.2 | 1.1        1.2 | 2.1        2.2 | 3.1          3.2



## Static routing

Setup:

    ./setup-net.sh
    ./setup-static.sh

Show routing tables:

    # ip netns exec R01 ip route
    10.0.0.0/24 dev R01.0 proto kernel scope link src 10.0.0.2
    10.0.1.0/24 dev R01.1 proto kernel scope link src 10.0.1.1
    10.0.2.0/24 nhid 10 via 10.0.1.2 dev R01.1 proto rip metric 20
    10.0.3.0/24 nhid 10 via 10.0.1.2 dev R01.1 proto rip metric 20

Ping Server:

    # ping -c1 10.0.3.2
    PING 10.0.3.2 (10.0.3.2) 56(84) bytes of data.
    64 bytes from 10.0.3.2: icmp_seq=1 ttl=61 time=0.043 ms

    --- 10.0.3.2 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.043/0.043/0.043/0.000 ms

Traceroute:

    # traceroute 10.0.3.2
    traceroute to 10.0.3.2 (10.0.3.2), 30 hops max, 60 byte packets
    1  10.0.0.2 (10.0.0.2)  0.039 ms  0.004 ms  0.004 ms
    2  10.0.1.2 (10.0.1.2)  0.013 ms  0.005 ms  0.004 ms
    3  10.0.2.2 (10.0.2.2)  0.012 ms  0.005 ms  0.006 ms
    4  10.0.3.2 (10.0.3.2)  0.011 ms  0.006 ms  0.006 ms

Netcat (echo):

    # ip netns exec Server ncat -lp 2000 -c cat

    Other shell:

    $ ncat 10.0.3.2 2000
    hello
    hello  # reply


## RIP

Setup:

    ./setup-net.sh
    ./setup-rip.sh

Check config:

    # ip netns exec R01 vtysh -c "show running-config"
    Building configuration...

    Current configuration:
    !
    frr version 8.4.4
    frr defaults traditional
    hostname fry
    no ipv6 forwarding
    service integrated-vtysh-config
    !
    router rip
    network 10.0.2.0/24
    network 10.0.3.0/24
    redistribute connected
    exit
    !
    end

Show basic routing info:

    # ip netns exec R01 vtysh -c "show ip route"
    Codes: K - kernel route, C - connected, S - static, R - RIP,
        O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
        T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
        f - OpenFabric,
        > - selected route, * - FIB route, q - queued, r - rejected, b - backup
        t - trapped, o - offload failure

    R>* 10.0.0.0/24 [120/3] via 10.0.2.1, R23.2, weight 1, 00:03:49
    R>* 10.0.1.0/24 [120/2] via 10.0.2.1, R23.2, weight 1, 00:03:49
    C>* 10.0.2.0/24 is directly connected, R23.2, 00:03:50
    C>* 10.0.3.0/24 is directly connected, R23.3, 00:03:50

Show RIP info:

    # ip netns exec R01 vtysh -c "show ip rip"
    Codes: R - RIP, C - connected, S - Static, O - OSPF, B - BGP
    Sub-codes:
        (n) - normal, (s) - static, (d) - default, (r) - redistribute,
        (i) - interface

        Network            Next Hop         Metric From            Tag Time
    R(n) 10.0.0.0/24        10.0.2.1              3 10.0.2.1          0 02:42
    R(n) 10.0.1.0/24        10.0.2.1              2 10.0.2.1          0 02:42
    C(i) 10.0.2.0/24        0.0.0.0               1 self              0
    C(i) 10.0.3.0/24        0.0.0.0               1 self              0
