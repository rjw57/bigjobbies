#!/bin/bash
#
# Run when the

# exit immediately on error
set -e

config_file=/repo/.jobbies.yaml

# Get utility functions
. util.sh

cd /repo

section Setup virtualenv

wrap pip3 install --user virtualenv
wrap python3 -m virtualenv -p "$(which python3)" /tmp/venv

info Activating virtualenv
. /tmp/venv/bin/activate

# A bit of a hack to treat a single string as a single item list
get_values() (
    shyaml get-values-0 "$@" <"${config_file}" 2>/dev/null || \
        (shyaml get-value "$@" <"${config_file}" && printf '\0')
)

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

