#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker run --init --rm -d \
		--network meta-extract_default \
		--name "rq$counter" \
		-v /data/thread0:/data/thread0 \
		alpine/rq-tika
	((counter++))
done
