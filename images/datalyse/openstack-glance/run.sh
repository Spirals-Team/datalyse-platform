#!/bin/bash
set -e
set -o xtrace

if [ -z "$GLANCE_PASSWORD" ]; then
	echo >&2 'error: missing required GLANCE_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e GLANCE_PASSWORD=... ?'
	exit 1
fi

if [ -z "$KEYSTONE_PASSWORD" ]; then
	echo >&2 'error: missing required KEYSTONE_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e KEYSTONE_PASSWORD=... ?'
	exit 1
fi

if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
	echo >&2 'error: missing required MYSQL_ROOT_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e MYSQL_ROOT_PASSWORD=... ?'
	exit 1
fi

if [ -z "$RABBITMQ_PASSWORD" ]; then
	echo >&2 'error: missing required RABBITMQ_PASSWORD environment variable'
	echo >&2 '  Did you forget to -e RABBITMQ_PASSWORD=... ?'
	exit 1
fi

/usr/bin/ansible-playbook /bootstrap-pre.yml

services=("glance-api" "glance-registry")
pids=()
logs=()

for i in ${services[@]}; do
	log="/$i.log"

	/usr/bin/$i --config-file /etc/glance/$i.conf --debug > $log 2>&1 &

  pids+=($!)
	logs+=($log)
done

/mtail.sh ${logs[@]} &

/usr/bin/ansible-playbook /bootstrap-post.yml

wait ${pids[@]}
