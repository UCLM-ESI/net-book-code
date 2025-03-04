

## Topology:

            0.0/24           1.0/24           2.0/24           3.0/24
    host ------------ R01 ------------ R12 ------------ R23 ------------ Server
       0.2         0.3 | 1.2        1.3 | 2.2        2.3 | 3.2          3.3


## Static routing

Setup:

    $ make restart
    $ sudo ./fix-bridge-addrs.sh
    $ ./setup-static.sh

Show routing tables:

    $ docker compose exec r01 ip route
    default via 10.0.1.3 dev eth1
    10.0.0.0/24 dev eth0 proto kernel scope link src 10.0.0.3
    10.0.1.0/24 dev eth1 proto kernel scope link src 10.0.1.2

Ping Server:

    $ ping 10.0.3.2
    PING 10.0.3.2 (10.0.3.2) 56(84) bytes of data.
    64 bytes from 10.0.3.2: icmp_seq=1 ttl=62 time=0.104 ms

Traceroute Server:

    $ traceroute 10.0.3.2
    traceroute to 10.0.3.2 (10.0.3.2), 30 hops max, 60 byte packets
    1  10.0.0.3 (10.0.0.3)  0.585 ms  0.432 ms  0.012 ms
    2  10.0.1.3 (10.0.1.3)  0.031 ms  0.016 ms  0.010 ms
    3  10.0.3.2 (10.0.3.2)  0.022 ms  0.013 ms  0.013 ms


## RIP

Setup:

    $ make restart
    $ sudo ./fix-bridge-addrs.sh
    $ ./setup-rip.sh

Check config:

    $ docker compose exec r01 vtysh -c "show running-config"
    Building configuration...

    Current configuration:
    !
    frr version 8.4.4
    frr defaults traditional
    hostname r01
    no ipv6 forwarding
    service integrated-vtysh-config
    !
    router rip
    network 10.0.0.0/24
    network 10.0.1.0/24
    redistribute connected
    exit
    !
    end

Show basic routing info:

    $ docker compose exec r01 vtysh -c "show ip route"
    Codes: K - kernel route, C - connected, S - static, R - RIP,
        O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
        T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
        f - OpenFabric,
        > - selected route, * - FIB route, q - queued, r - rejected, b - backup
        t - trapped, o - offload failure

    C>* 10.0.0.0/24 is directly connected, eth0, 00:01:26
    C>* 10.0.1.0/24 is directly connected, eth1, 00:01:26
    R>* 10.0.2.0/24 [120/2] via 10.0.1.3, eth1, weight 1, 00:00:30
    R>* 10.0.3.0/24 [120/3] via 10.0.1.3, eth1, weight 1, 00:00:30

Show RIP info:

    $ docker compose exec r01 vtysh -c "show ip rip"
    Codes: R - RIP, C - connected, S - Static, O - OSPF, B - BGP
    Sub-codes:
        (n) - normal, (s) - static, (d) - default, (r) - redistribute,
        (i) - interface

        Network            Next Hop         Metric From            Tag Time
    C(i) 10.0.0.0/24        0.0.0.0               1 self              0
    C(i) 10.0.1.0/24        0.0.0.0               1 self              0
    R(n) 10.0.2.0/24        10.0.1.3              2 10.0.1.3          0 02:33
    R(n) 10.0.3.0/24        10.0.1.3              3 10.0.1.3          0 02:33
