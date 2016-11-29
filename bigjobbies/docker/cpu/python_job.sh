#!/bin/bash
#
# Run when the

# exit immediately on error
set -e

config_file=/repo/.jobbies.yaml

# Get utility functions
. util.sh

# This is to make sure we don't use the Python within the virtualenv
system_python=$(which python3)
jobbieget="$PWD/jobbieget.py"

get_values() ( "${system_python}" "${jobbieget}" "$@" <"${config_file}" )

cd /repo

section Setup virtualenv

wrap pip3 install --user virtualenv
wrap python3 -m virtualenv -p "$(which python3)" /tmp/venv

info Activating virtualenv
. /tmp/venv/bin/activate

wrap python --version
wrap pip --version

section Install

get_values install 'pip install .' | \
    (while IFS= read -r -d '' cmd; do wrap $cmd; done)

section Run

if [ -z "$(get_values script)" ]; then
    error No run script specified in ${config_file}
    exit 1
fi

get_values script | \
    (while IFS= read -r -d '' cmd; do wrap $cmd; done)

