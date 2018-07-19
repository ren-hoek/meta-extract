import tempfile
import os
from rq import Queue
from redis import Redis
import pymongo as py
import docproc.darknet as dk


dk.dk_net = dk.load_net("cfg/yolov3.cfg", "yolov3.weights", 0)
dk.dk_meta = dk.load_meta("cfg/coco.data")

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for img_id in col.find({"$and": [
        {"Content-Type.Content": "image/jpeg"},
        {"raw_file": {"$exists": True}}]}, {}):
    job = dk.insert_yolo_tags(img_id, False)
    print(job)

