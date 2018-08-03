#!/bin/bash
#
# Build the worker docker image
#


IMAGE=ubuntu/rq-htmlimage

# tar the python code
tar -czvf docproc.tar.gz ../docproc

# build the docker image
docker build -t "$IMAGE" .
