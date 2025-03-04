FROM debian:latest

RUN apt-get update && \
    apt-get install -y iproute2 procps frr && \
    rm -rf /var/lib/apt/lists/*

CMD ip route del default && \
    sysctl -w net.ipv4.ip_forward=1 && \
    exec sleep infinity
