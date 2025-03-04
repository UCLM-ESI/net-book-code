FROM debian:latest

RUN apt-get update && \
    apt-get install -y iproute2 iputils-ping traceroute tshark procps frr && \
    rm -rf /var/lib/apt/lists/*

CMD ip route del default && \
    exec sleep infinity
