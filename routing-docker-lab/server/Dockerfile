FROM debian:latest

RUN apt-get update && \
    apt-get install -y iproute2 iputils-ping traceroute tshark ncat && \
    rm -rf /var/lib/apt/lists/*

CMD ip route del default && \
    ip route add default via 10.0.3.2 && \
    exec sleep infinity
