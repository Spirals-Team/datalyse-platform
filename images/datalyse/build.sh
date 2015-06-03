#!/bin/bash
set -e
# set -o xtrace

# ---------------------------------------------------------------------

INVENTORY="inventory"
PREFIX="datalyse"
PORT=2375

# ---------------------------------------------------------------------

if [ $# -lt 1 ]; then
  echo "Usage $0 <docker-image-directory> [<docker-image-directory> ... [<docker-image-directory]]"
  exit 1
fi

function abspath {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

function build {
  host=$1
  dockerfiledir=$2

  if [ ! -d "$dockerfiledir" ]; then
    echo "$dockerfiledir: no such a directory"
    exit 1
  fi

  if [ ! -f "$dockerfiledir/Dockerfile" ]; then
    echo "$dockerfiledir/Dockerfile: no such a file"
    exit 1
  fi

  name=$(basename $(abspath "$dockerfiledir"))
  imagename="$PREFIX/$name"

  docker -H $host:$PORT build -t $imagename $dockerfiledir #2>&1 | gsed -e "s/^/[\x1b[32m $name \x1b[0m]: &/"

}

inventory_file="$(dirname $(dirname $(abspath $0)))/$INVENTORY"
hosts=$(cat $inventory_file | grep ansible_ssh_host | awk '{split($2,a,"="); print a[2];}')

echo $hosts

for dockerfiledir in $@; do
  for host in $hosts; do
    echo "Building '$dockerfiledir' on '$host':"
    build $host $dockerfiledir
  done
done