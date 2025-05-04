#!/bin/bash

# add "server1" default route
docker exec server1 ip route add default via 10.0.5.2
docker exec server1 ip route add 224.0.0.0/4 via 10.0.5.2

# add "server2" default route
docker exec server2 ip route add default via 10.0.3.2
docker exec server2 ip route add 224.0.0.0/4 via 10.0.3.2

# add route for 10.0/16 for "host"
ip route replace 10.0.0.0/16 via 10.0.0.3
ip route replace 224.0.0.0/4 via 10.0.0.3
