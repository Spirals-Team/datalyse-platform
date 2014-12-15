#!/bin/bash
set -e

VAGRANT_INVENTORY="vagrant-inventory"

IP=$(vagrant ssh -c "ifconfig eth1" 2>&1 | grep "inet addr" | awk '{print $2}' | awk -F ':' '{print $2}')

[ -f $VAGRANT_INVENTORY ] || cat > $VAGRANT_INVENTORY <<EOF
[all:vars]
ansible_ssh_user=vagrant
ansible_ssh_private_key_file=$HOME/.vagrant.d/insecure_private_key

[all]
$IP 
EOF

echo "export ANSIBLE_HOST_KEY_CHECKING=False"
echo "export DOCKER_HOST=$IP:2375"