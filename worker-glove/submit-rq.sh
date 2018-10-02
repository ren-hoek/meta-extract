#!/bin/bash
docker run -d \
    --rm \
    --network metaextract_default \
    --name submit-glove \
    -v /data:/data \
    alpine/rq-glove $1

