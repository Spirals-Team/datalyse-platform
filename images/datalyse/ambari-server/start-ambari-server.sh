#!/bin/bash
set -e

PID=/var/run/ambari-server/ambari-server.pid
LOG=/var/log/ambari-server/ambari-server.log
TIMEOUT=60

/etc/init.d/ntpd start
/usr/sbin/ambari-server start --debug

try=0
while [ ! -f "$PID" ] && [ $try -le $TIMEOUT ]; do 
	sleep 1
	try=$((try+1))
done

/join.sh $PID $LOG
