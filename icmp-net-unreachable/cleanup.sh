#!/bin/bash

ip route del 10.10.0.0/16
ip link del veth-host
ip netns del r1
