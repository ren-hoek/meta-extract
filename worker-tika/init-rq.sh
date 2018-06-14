#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker run --init --rm -d --network jupyterhub --name "rq$counter" alpine/rq-tika
	((counter++))
done
