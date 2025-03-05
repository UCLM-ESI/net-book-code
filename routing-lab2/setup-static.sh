#!/bin/bash

docker compose exec r1 ip route add default via 10.0.3.3
docker compose exec r2 ip route add 10.0.0.0/24 via 10.0.1.2
docker compose exec r2 ip route add default via 10.0.2.3
docker compose exec r3 ip route add default via 10.0.3.2
