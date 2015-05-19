#!/bin/bash

if [ $# -lt 1 ]; then
  echo >&2 "Usage: $0 <file1> [<file2>] ... [<fileN>]"
  exit 1
fi

pids=()

function finish {
  kill ${pids[@]}
}

for f in $@; do
  # the '\x1b' is a sed escape code; '[32m' is greed '[0m' resets
  tail -F $f | sed -e "s/^/[\x1b[32m $(basename $f) \x1b[0m]: &/" &
  pids+=($!)
done

trap finish EXIT

wait ${pids[@]}
