#!/bin/bash
docker run -d \
    --rm \
    --network metaextract_default \
    --name yolocpu \
    --hostname yolocpu \
    analysis/rq-yolocpu $1

