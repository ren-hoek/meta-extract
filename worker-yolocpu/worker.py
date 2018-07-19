import os
from redis import Redis
from rq import Worker, Queue, Connection
import docproc.darknet as dk

dk.net = dk.load_net("cfg/yolov3.cfg", "yolov3.weights", 0)
dk.meta = dk.load_meta("cfg/coco.data")

listen = ['high', 'default', 'low']

redis_conn = Redis(host='redis')

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
