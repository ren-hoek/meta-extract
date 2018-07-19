nvidia-docker run -it \
    --rm \
	-e LD_LIBRARY_PATH='/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/cuda-9.0/lib64' \
	--network metaextract_default \
	--name yologpu \
	--hostname yologpu \
	analysis/rq-yologpu

