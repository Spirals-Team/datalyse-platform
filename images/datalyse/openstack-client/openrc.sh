#!/bin/bash

# USAGE: source openrc.sh <user> <pass> <tenant>

if [[ -n "$1" ]]; then
    OS_USERNAME=$1
fi

if [[ -n "$2" ]]; then
    OS_PASSWORD=$2
fi

if [[ -n "$3" ]]; then
    OS_TENANT_NAME=$3
fi

export OS_USERNAME=${OS_USERNAME:-admin}
export OS_PASSWORD=${OS_PASSWORD:-stack}
export OS_TENANT_NAME=${OS_TENANT_NAME:-admin}
export OS_AUTH_URL="http://$KEYSTONE_KEYSTONE_MASTER_HOST:5000/v2.0"
