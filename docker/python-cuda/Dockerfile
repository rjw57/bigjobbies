FROM nvidia/cuda:cudnn-ubuntu14.04
MAINTAINER Rich Wareham <rjw57@cam.ac.uk>

# /scratch on Yoshi will be mounted here read only
VOLUME /data

# /scratch/${USER} on Yoshi will be mounted here read-write
VOLUME /workspace

# set up a basic dev. environment and utilities required for scripts
RUN apt-get -y update && \
    apt-get -y install git build-essential python python3 python3-pip

# Copy the run script into the container
COPY user_run.sh .
COPY root_run.sh .
COPY util.sh .
ENTRYPOINT ./root_run.sh
