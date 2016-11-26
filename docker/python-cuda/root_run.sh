#!/bin/bash
#
# This script is run as the root user within the container. It sets up an
# unprivileged user with the same uid/gid as the user launching the container
# and then transfers control to another script as that user.
#
# The rationale for this trampoline-like behaviour is that we want files created
# as part of the job to be owned by the launching user so that they can
# access/move/delete them afterwards. If everything created by the job were
# owned by root then that would be awkward afterwards.
#
# The script also reads the "apt-packages.txt" file in the project directory. If
# this file exists it lists packages, one per line, which should be installed
# via apt into the container before passing control to the unprivileged script.

# Exit on first error
set -e

# Get utility functions
. util.sh

section Prepare environment

# These environment variables are passed into the container through docker run
export DOCKER_USER_UID=${DOCKER_USER_UID:-1000}
export DOCKER_USER_GID=${DOCKER_USER_GID:-1000}

info Creating worker user and group

# Create a group for the non-root user
wrap groupadd --gid "${DOCKER_USER_GID}" worker

# Create non-root user to do actual work
wrap useradd --create-home \
	--gid "${DOCKER_USER_GID}" --uid "${DOCKER_USER_UID}" \
	worker

# handle GIT_BRANCH environment
if [ ! -z "${GIT_BRANCH}" ]; then
	clone_args="${clone_args} --branch '${GIT_BRANCH}'"
fi

section Clone repository

# clone the repo as the new user
mkdir /repo
chown worker:worker /repo
git_cmd="git clone --progress --depth=1 --recursive ${clone_args} '${GIT_REPO}' /repo"
logcmd "${git_cmd}" su -c "${git_cmd}" worker

section Install packages

# Install any packages specified by the user
pkg_list=/repo/apt-packages.txt
if [ -f "${pkg_list}" ]; then
	logcmd \
		"installing packages specified in ${pkg_list}" \
		xargs -d '\n' apt-get -y install <"${pkg_list}"
else
	info "no apt packages in ${pkg_list}"
	info "add package names, one per line, to this file to install them"
fi

# Run the unprivileged side of the script
su -c '/bin/bash ./user_run.sh' worker
