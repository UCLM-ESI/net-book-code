FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y procps iproute2 iputils-ping traceroute tshark frr && \
    rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", \
    "ip route del default && \
    sysctl -w net.ipv4.ip_forward=1 && \
    /usr/lib/frr/zebra"]
