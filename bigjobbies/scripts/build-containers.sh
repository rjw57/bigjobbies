#!/bin/bash
#$ -l queue-priority=cuda
#$ -S /bin/bash
set -e

# Wrap a command such that standard output lines are prefixed by "O:" and
# standard error by "E:".
#
# Inspired by:
# http://serverfault.com/questions/59262
# http://stackoverflow.com/questions/9112979
logcmd()(
    set -o pipefail;
    echo "C:$1";
    shift
    { "$@" 2>&3 | sed 's,^,O:,' >&2; } 3>&1 1>&2 | sed 's,^,E:,'
)

wrap()(
    logcmd "$*" "$@"
)

info()( echo "I:$*" )

error()( echo "E:$*" )

section()( echo "S:$*" )

if [ -z "${CONTAINER_DIR}" ]; then
	error "CONTAINER_DIR was not set"
	exit 1
fi

CONTAINERS="cuda"

for container in $CONTAINERS; do
	CONTAINER_NAME="${IMAGE_PREFIX}:${container}"
	section "Building container ${CONTAINER_NAME}"
	wrap docker build -t "${IMAGE_TAG}" -t "${CONTAINER_NAME}" ${CONTAINER_DIR}/${container}
	info "successfully built container ${CONTAINER_NAME}"
done
