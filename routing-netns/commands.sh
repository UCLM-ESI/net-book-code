

remove-all-veth() {
    for iface in $(ip -o link show type veth | awk '{print $2}' | sed 's/://;s/@.*//'); do
        ip link delete $iface;
    done
}

remove-all-ns() {
    for ns in $(ip netns list); do
        ip netns del $ns;
    done
}
