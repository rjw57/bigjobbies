#!/bin/bash
#
# This script is invoked from root_run.sh and is the unprivileged half of the
# container entrypoint. It prints some diagnostic information and then arranges
# for tox to be run in the project directory. It is then up to the tox
# configuration to Do The Right Thing.

# exit immediately on error
set -e

# set up global path
export PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

# set up local path
export PATH=$HOME/.local/bin:$PATH
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH

# set up cache directory in a persistent location
export XDG_CACHE_HOME=/workspace/cache

# save any extra arguments to script
cli_args="$@"

# where to find pip
PIP=${PIP:-pip3}
if [ -z "${PIP}" ]; then
	echo "-- pip not found on PATH. Aborting" >&2
	exit 1
fi

# change to repo directory
cd /repo

# show information on which GPU we're using
echo "-- GPU information:"
nvidia-smi

# show information on environment
echo "-- environment variables:"
env

echo "-- project directory in container is $PWD"

# check there is a tox file
if [ ! -f tox.ini ]; then
	echo "-- No tox.ini file found. Aborting." >&2
	exit 1
fi

# check tox is installed
if [ -z "$(which tox)" ]; then
	echo "-- tox not on PATH. Installing via pip."
	"${PIP}" install --user tox
fi

if [ -z "$(which tox)" ]; then
	echo "-- tox not found on PATH. Ensure it is installed." >&2
fi

echo "-- running: tox $@"
exec tox $@
