FROM ubuntu:14.04
MAINTAINER Rich Wareham <rjw57@cam.ac.uk>

# /scratch on Yoshi will be mounted here read only
VOLUME /data

# /scratch/${USER} on Yoshi will be mounted here read-write
VOLUME /workspace

# set up a basic dev. environment and utilities required for scripts
RUN apt-get -y update && \
    apt-get -y install git build-essential python python3 python3-pip \
        python3-yaml python3-docopt

# This argument is the "namespace" that all the labels should live in for the
# bigjobbies containers in general.
ARG LABEL_NS=com.richwareham.bigjobbies.

ARG USER

LABEL ${LABEL_NS}worker=1 \
    ${LABEL_NS}user=${USER} \
    ${LABEL_NS}type=cpu \
    ${LABEL_NS}os=ubuntu14.04

# Copy the run script into the container
COPY *.sh *.py ./
ENTRYPOINT ./root_run.sh
