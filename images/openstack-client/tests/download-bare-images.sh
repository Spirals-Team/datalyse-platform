#!/bin/bash
set -e
set -o xtrace

if ! glance image-show cirros-0.3.2-x86_64; then
  glance image-create \
    --copy-from http://cdn.download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img \
    --is-public=True \
    --container-format=bare \
    --disk-format=qcow2 \
    --name cirros-0.3.2-x86_64
fi