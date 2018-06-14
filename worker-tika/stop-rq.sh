#!/bin/bash
counter=1
until [ $counter -gt $1 ]
do
	docker stop "rq$counter"
	((counter++))
done
