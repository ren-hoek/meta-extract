#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker run --rm -d --network jupyterhub --name "rq$1" alpine/rq-work
	((counter++))
done
