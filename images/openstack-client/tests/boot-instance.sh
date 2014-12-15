#!/bin/bash
set -e
set -o xtrace

nova boot i1 \
  --flavor m1.tiny \
  --image busybox \
  --nic net-id=$(nova network-list | awk '/ demo-net / {print $2}') \
  --security-group default \
  --key-name admin-key