# Notes
This worker detects and creates metadata on entities detected within images using CPU.

## Darknet
The worker use the [Darknet](https://pjreddie.com/darknet/) neural network framework to apply the [YOLO](https://pjreddie.com/darknet/yolo/) 
object detector to images. This worker is designed to be run on an CPU.

## Running

### RQ Submitting 
As Darknet needs to be installed to submit jobs to the queue, we need to the specific worker to submit the jobs instead of the more generic jpytika container
```bash
./submit.sh rqyolo.py
```
Once submitted starting workers is the same as for other processing
```bash
./init-rq.sh 3
```
Then to stop the worker
```bash
./stop-rq.sh 3
```
