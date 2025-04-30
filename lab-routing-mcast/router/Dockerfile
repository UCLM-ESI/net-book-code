FROM debian:latest

RUN apt-get update && \
    apt-get install -y procps iproute2 iputils-ping traceroute tshark frr nano && \
    rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", \
    "ip route del default && \
    sysctl -w net.ipv4.ip_forward=1 && \
    sed -i 's/pimd=no/pimd=yes/g' /etc/frr/daemons && \
    /usr/lib/frr/zebra"]
