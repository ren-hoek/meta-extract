# Notes
This worker detects and creates metadata on entities detected within images using GPU acceleration.

## Darknet
The worker use the [Darknet](https://pjreddie.com/darknet/) neural network framework to apply the [YOLO](https://pjreddie.com/darknet/yolo/) 
object detector to images. This worker is designed to be run on an NVIDIA CUDA enabled GPU.

## Prerequisites
In order to use this work an [NVIDIA CUDA enabled GPU](https://developer.nvidia.com/cuda-gpus) is required and nvidia-docker must be 
installed. It currently uses [nvidia-docker v1.0](https://github.com/NVIDIA/nvidia-docker/tree/1.0)

## Queueing
Currently when implemented with the RQ system on a GPU the YOLO model has to be reloaded every image, this causes a considerable overhead.
Therefore the most effcient way to run the process is to directly submit the job to the worker.

## Running

### RQ Submitting 
As Darknet needs to be installed to submit jobs to the queue, we need to the specific worker to submit the jobs instead of the more generic jpytika container
```bash
./init-gpu.sh rqyolo.py
```
Then to start the GPU enabled worker
```bash
./init-gpu.sh
```
Then to stop the worker
```bash
./stop-gpu.sh
```

### Direct Submitting 
Instead of using RQ, as mentioned above the most effcient way to run the process is to driectly submit the job to the worker
```bash
./init-gpu wkyolo.py
```
