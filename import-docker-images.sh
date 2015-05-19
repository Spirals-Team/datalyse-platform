#!/bin/bash
set -e
set -o xtrace

IMAGES="busybox rastasheep/ubuntu-sshd"

for image in $IMAGES; do
  if ! glance image-show; then
    docker pull $image
    docker save $image | glance image-create \
      --is-public=True \
      --container-format=docker \
      --disk-format=raw \
      --name "$image"
  fi
done
