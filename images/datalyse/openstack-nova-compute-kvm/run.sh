#!/bin/bash
set -e
set -o xtrace

if [ -z "$NOVA_PASSWORD" ]; then
	echo >&2 'error: missing required NOVA_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e NOVA_PASSWORD=... ?'
	exit 1
fi

if [ -z "$KEYSTONE_PASSWORD" ]; then
	echo >&2 'error: missing required KEYSTONE_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e KEYSTONE_PASSWORD=... ?'
	exit 1
fi

if [ -z "$RABBITMQ_PASSWORD" ]; then
	echo >&2 'error: missing required RABBITMQ_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e RABBITMQ_PASSWORD=... ?'
	exit 1
fi

/usr/bin/ansible-playbook /bootstrap-pre.yml

services=("nova-compute" "nova-api-metadata" "nova-network")
pids=()
logs=()

# start libvirtd
/usr/sbin/libvirtd --verbose > /libvirtd.log 2>&1 &
pids+=($!)
logs+=(/libvirtd.log)

for i in ${services[@]}; do
	log="/$i.log"

	/usr/bin/$i --config-file /etc/nova/nova.conf --debug > $log 2>&1 &

  pids+=($!)
	logs+=($log)
done

/mtail.sh ${logs[@]} &

wait ${pids[@]}