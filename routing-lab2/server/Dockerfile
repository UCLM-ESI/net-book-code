FROM lab2-router

RUN apt-get update && \
    apt-get install -y ncat && \
    rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", \
    "ip route del default && \
    exec sleep infinity"]
