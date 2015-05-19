#/bin/sh
set -e
set -o xtrace

function abspath {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

if [ $# -lt 1 ]; then
	echo "Usage $0 <docker-image-directory> [<docker-image-directory> ... [<docker-image-directory]]"
	exit 1
fi

for dockerfiledir in "$@"; do
	if [ ! -d "$dockerfiledir" ]; then
		echo "$dockerfiledir: no such a directory"
		exit 1
	fi
	if [ ! -f "$dockerfiledir/Dockerfile" ]; then
		echo "$dockerfiledir/Dockerfile: no such a file"
		exit 1
	fi

	name=$(basename $(abspath "$dockerfiledir"))
	prefix=$(basename $(dirname $(abspath "$dockerfiledir")))
	imagename="$prefix/$name"

	docker build -t $imagename $dockerfiledir #2>&1 | gsed -e "s/^/[\x1b[32m $name \x1b[0m]: &/"
done
