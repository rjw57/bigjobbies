#$ -S /bin/bash
#$ -l queue-priority=cuda

if [ -z "${X_SGE_CUDA_DEVICE}" ]; then
	cat >&2 <<EOL
-- No GPU device was specified in the grid engine configuration. Check that you
-- submitted the job to the correct queue and that the X_SGE_CUDA_DEVICE
-- environment variable was set.
-- Job environment:
EOL
	env >&2
	exit 1
fi

if [ -z "${GIT_REPO}" ]; then
	cat >&2 <<EOL
-- No git reporistory was specified. Use the GIT_REPO environment variable to
-- define the repository to clone.
-- Job environment:
EOL
	env >&2
	exit 1
fi

if [ -z "${CONTAINER_TAG}" ]; then
	cat >&2 <<EOL
-- No container tag was specified.
EOL
	env >&2
	exit 1
fi

# Get the user primary group id or fallback to the UID
DOCKER_USER_GID=$(id -g)
DOCKER_USER_GID=${DOCKER_USER_GID:-${DOCKER_USER_UID}}

echo "S:Launching container"
echo "I:Container image: ${CONTAINER_TAG}"
echo "I:GIT_REPO=${GIT_REPO}"
echo "I:GIT_BRANCH=${GIT_BRANCH}"
echo "I:CONTAINER_TAG=${CONTAINER_TAG}"

NV_GPU="${X_SGE_CUDA_DEVICE}" nvidia-docker run \
	--rm \
	-e GIT_REPO -e GIT_BRANCH=${GIT_BRANCH} \
	-e NSLOTS="${NSLOTS}" -e NHOSTS="${NHOSTS}" -e JOB_ID="${JOB_ID}" \
	-e JOB_NAME="${JOB_NAME}" -e REQUEST="${REQUEST}" \
	-e QUEUE="${QUEUE}" -e SGE_TASK_ID="${SGE_TASK_ID}" \
	-e SGE_TASK_FIRST="${SGE_TASK_FIRST}" -e SGE_TASK_LAST="${SGE_TASK_LAST}" \
	-e SGE_TASK_STEPSIZE="${SGE_TASK_STEPSIZE}" -e SGR_ARCH="${SGR_ARCH}" \
	-e DOCKER_USER_UID=${UID} \
	-e DOCKER_USER_GID=${DOCKER_USER_GID} \
	-v /scratch:/data:ro \
	-v /scratch/$USER:/workspace \
	${DOCKER_RUN_ARGS} \
        ${CONTAINER_TAG}
