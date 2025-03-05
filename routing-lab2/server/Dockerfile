FROM router

RUN apt-get update && \
    apt-get install -y ncat && \
    rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", \
    "ip route del default && \
    ip route add default via 10.0.4.2 && \
    exec sleep infinity"]
