#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker run --init --rm -d \
		--network jupyterhub \
		--name "rq$counter" \
		-v /home/gavin/Downloads/files:/home/gavin/Downloads/files \
		alpine/rq-tika
	((counter++))
done
