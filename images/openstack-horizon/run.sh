#!/bin/bash
set -e
set -o xtrace

if [ -z "$KEYSTONE_KEYSTONE_MASTER_HOST" ]; then
  echo >&2 'error: missing required KEYSTONE_KEYSTONE_MASTER_HOST environment variable'
  echo >&2 '  Did you forget to set -e KEYSTONE_KEYSTONE_MASTER_HOST ?'
  exit 1
fi

sed -i "s/^OPENSTACK_HOST = .*$/OPENSTACK_HOST = \"$KEYSTONE_KEYSTONE_MASTER_HOST\"/" /etc/openstack-dashboard/local_settings.py
sed -i "s/'level': 'INFO'/'level': 'DEBUG'/" /etc/openstack-dashboard/local_settings.py
sed -i "s/DEBUG = False/DEBUG = True/" /etc/openstack-dashboard/local_settings.py

# Make sure we're not confused by old, incompletely-shutdown httpd
# context after restarting the container.  httpd won't start correctly
# if it thinks it is already running.
rm -rf /run/httpd/*

pids=()

memcached -u daemon &
pids+=($!)

/usr/sbin/apachectl -D FOREGROUND &
pids+=($!)

/mtail.sh /var/log/apache2/access.log /var/log/apache2/error.log &

wait ${pids[@]}