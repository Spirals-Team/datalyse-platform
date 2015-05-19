#!/bin/bash
 set -e

# http://stackoverflow.com/questions/1058047/wait-for-any-process-to-finish
function anywait {
  while kill -0 "$1"; do
    sleep 1
  done
}
 
pid=$1
log=$2

cat $pid

# perhaps it is a pid file
if [ -f $pid ]; then
  pid=$(cat $pid)
fi

if [ -f "$log" ]; then
  tail -f -n +0 "$log" &
fi

# cannot use `wait $pid` since this script does not own the process
anywait $pid
kill $!