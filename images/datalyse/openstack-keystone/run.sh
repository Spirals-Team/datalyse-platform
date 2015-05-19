#!/bin/bash
set -e
set -o xtrace

REQS="KEY"

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

# these are steps to be done before keystone is run (e.g. mysql)
/usr/bin/ansible-playbook /bootstrap-pre.yml

/usr/bin/keystone-all --config-file /etc/keystone/keystone.conf --debug > keystone.log 2>&1 &
pid=$!

/mtail.sh keystone.log &

# these are steps to be done after keystone is run (e.g., tenant, service)
/usr/bin/ansible-playbook /bootstrap-post.yml

wait $pid
