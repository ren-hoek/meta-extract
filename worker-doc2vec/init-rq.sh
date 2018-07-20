#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker run --init --rm -d \
		--network metaextract_default \
		--name "rq$counter" \
		-v /data:/data \
		alpine/rq-doc2vec
	((counter++))
done
