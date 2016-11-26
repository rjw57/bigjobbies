#!/bin/bash
#
# This script is invoked from root_run.sh and is the unprivileged half of the
# container entrypoint. It prints some diagnostic information and then arranges
# for tox to be run in the project directory. It is then up to the tox
# configuration to Do The Right Thing.

# exit immediately on error
set -e

# Get utility functions
. util.sh

# set up global path
export PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

# set up local path
export PATH=$HOME/.local/bin:$PATH
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH

# set up cache directory in a persistent location
export XDG_CACHE_HOME=/workspace/cache

# show information on which GPU we're using
section GPU information
wrap nvidia-smi

# show information on environment
section Environment variables
wrap env

config_file=/repo/.jobbies.yaml
info "Parsing ${config_file} file"
if [ ! -f "${config_file}" ]; then
    error The file ${config_file} was not found.
    error The job cannot proceed without it.
    exit 1
fi

language=$(shyaml get-value language '' <"${config_file}")
if [ -z ${language} ]; then
    error No language specified in ${config_file}
    exit 1
fi

case "${language}" in
    "python") exec ./python_job.sh
    ;;
    *) error "Unknown language: ${language}"
    ;;
esac
