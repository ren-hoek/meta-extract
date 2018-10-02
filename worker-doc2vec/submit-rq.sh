#!/bin/bash
docker run -d \
    --rm \
    --name submit-doc2vec \
    -v /data:/data \
    alpine/rq-doc2vec $1

