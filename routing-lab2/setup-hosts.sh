#!/bin/bash

# add route for 10.0/16 for "host"
ip route add 10.0.0.0/16 via 10.0.0.3

# add "server" default route for
docker exec server ip route add default via 10.0.4.2
