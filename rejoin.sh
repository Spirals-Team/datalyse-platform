#!/bin/bash

set -e

if ! docker info > /dev/null 2>&1; then
	echo "Unable to connect to docker"
	exit 1
fi

tmux_started=0

function is_container_running {
	[ "$(docker inspect -f '{{ .State.Running }}' $1 2>/dev/null)" == "true" ]
}

function new_window {
	if [ $tmux_started -eq 0 ]; then
		tmux new-session -d -s os -n "$@"
		tmux_started=1
	else
		tmux new-window -d -t os -n "$@"
	fi
}

function send {
	if is_container_running $1; then
  	tmux send -t $2 "$3" ENTER
  else
  	tmux send -t $2 "$3"
  fi
}

function new_log_window {
  new_window $1 bash
  send $2 $1 "docker logs -f $2"
}

function new_exec_window {
  new_window $1 bash
  send $2 $1 "docker exec -ti $2 $3"
}

function new_tail_window {
  new_window $1 bash
  send $2 $1 "docker exec -t $2 tail -F $3"		
}

function new_bash_window {
  new_window $1 bash
  send $2 $1 "docker exec -ti $2 bash"
}

################################################################################
# WINDOWS
################################################################################

new_exec_window db-console mysql "mysql --user=root --password=stack"
new_log_window db-log mysql
new_tail_window db-general /var/lib/mysql/mysqld-general.log
new_bash_window db-bash mysql

new_log_window rmq-server rabbitmq
new_tail_window rmq-log rabbitmq "/var/log/rabbitmq/rabbit@$(docker inspect -f '{{ .Config.Hostname }}' rabbitmq).log"
new_bash_window rmq-bash rabbitmq

new_tail_window k-all keystone /var/log/keystone/keystone-all.log
new_bash_window k-bash keystone

new_tail_window g-api /var/log/glance/api.log
new_tail_window g-registry /var/log/glance/registry.log
new_bash_window g-bash glance

new_tail_window n-api nova-controller /var/log/nova/nova-api.log
new_tail_window n-cert nova-controller /var/log/nova/nova-cert.log
new_tail_window n-conductor nova-controller /var/log/nova/nova-conductor.log
new_tail_window n-consoleauth nova-controller /var/log/nova/nova-consoleauth.log
new_tail_window n-manage nova-controller /var/log/nova/nova-manage.log
new_tail_window n-scheduler nova-controller /var/log/nova/nova-scheduler.log
new_bash_window n-bash nova-controller

new_tail_window n-cpu nova-compute-docker /var/log/nova/nova-compute.log
new_tail_window n-cpu-net nova-compute-docker /var/log/nova/nova-network.log
new_tail_window n-cpu-docker nova-compute-docker /var/log/docker.log
new_bash_window n-cpu-bash nova-compute-docker

new_tail_window h-error horizon /var/log/apache2/error.log
new_bash_window h-bash horizon

tmux attach-session -t os
tmux kill-session -t os