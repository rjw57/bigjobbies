#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_DIR=$(realpath "${DIR}/docker")
CONTAINERS="cuda"

for container in $CONTAINERS; do
	CONTAINER_NAME="${USER}:${container}"
	echo "-- building container: ${CONTAINER_NAME}"
	docker build -t "${CONTAINER_NAME}" ${DOCKER_DIR}/${container}
	echo "-- successfully built container: ${CONTAINER_NAME}"
done
