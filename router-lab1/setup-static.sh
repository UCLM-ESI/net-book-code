#!/bin/bash

docker compose exec r01 ip route add default via 10.0.1.3
docker compose exec r12 ip route add 10.0.0.0/24 via 10.0.1.2
docker compose exec r12 ip route add 10.0.3.0/24 via 10.0.2.3
docker compose exec r23 ip route add default via 10.0.2.2
