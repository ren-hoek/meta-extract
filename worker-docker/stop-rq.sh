#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker stop "rq$1"
	((counter++))
done
