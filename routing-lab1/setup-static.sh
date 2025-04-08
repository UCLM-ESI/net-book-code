#!/bin/bash

docker exec r1 ip route add default via 10.0.1.3
docker exec r2 ip route add 10.0.0.0/24 via 10.0.1.2
docker exec r2 ip route add 10.0.3.0/24 via 10.0.2.3
docker exec r3 ip route add default via 10.0.2.2
