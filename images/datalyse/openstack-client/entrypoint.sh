#!/bin/bash
set -e

PATTERNS="MYSQL RABBITMQ KEYSTONE GLANCE NOVA"

# captured environment variables
for p in $PATTERNS; do
  printenv | grep "$p" | sed 's/^/export &/' >> /root/variables
done

echo -e ". /root/variables\n" | cat - /root/.bashrc > /root/.bashrc.new
mv /root/.bashrc.new /root/.bashrc

/usr/sbin/sshd -D
