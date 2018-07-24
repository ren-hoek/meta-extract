#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker run --init --rm -d \
		--network metaextract_default \
		--name "rq$counter" \
		-v /data/:/data/ \
		ubuntu/rq-bottleneck
	((counter++))
done
