#!/bin/bash
#
# Build the worker docker image
#


IMAGE=alpine/rq-doc2vec

# tar the python code
tar -czvf docproc.tar.gz ../docproc

# build the docker image
docker build -t "$IMAGE" .
