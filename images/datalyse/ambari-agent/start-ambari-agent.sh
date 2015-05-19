#!/bin/bash
set -e

INI=/etc/ambari-agent/conf/ambari-agent.ini
PID=/var/run/ambari-agent/ambari-agent.pid
LOG=/var/log/ambari-agent/ambari-agent.log
TIMEOUT=60

AMBARI_SERVER=${AMBARI_SERVER:-$SERVER_PORT_8080_TCP_ADDR}

if [ -z "$AMBARI_SERVER" ]; then
  echo >&2 'error: missing required AMBARI_SERVER environment variable'
  echo >&2 '  Did you forget to -e AMBARI_SERVER=... ?'
  exit 1
fi

crudini --set $INI server hostname $AMBARI_SERVER
crudini --set $INI server url_port 8440
crudini --set $INI server secured_url_port 8441

/etc/init.d/ntpd start
/usr/sbin/ambari-agent start

try=0
while [ ! -f "$PID" ] && [ $try -le $TIMEOUT ]; do 
  sleep 1
  try=$((try+1))
done


/join.sh $PID $LOG