FROM nvidia/cuda:cudnn-ubuntu14.04
MAINTAINER Rich Wareham <rjw57@cam.ac.uk>

# /scratch on Yoshi will be mounted here read only
VOLUME /data

# /scratch/${USER} on Yoshi will be mounted here read-write
VOLUME /workspace

# set up a basic dev. environment and utilities required for scripts
RUN apt-get -y update && \
    apt-get -y install git build-essential python python3 python3-pip \
        python3-yaml python3-docopt

# Copy the run script into the container
COPY *.sh *.py ./
ENTRYPOINT ./root_run.sh
