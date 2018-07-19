import tempfile
import os
from rq import Queue
from redis import Redis
import pymongo as py
from docproc.darknet import insert_yolo_tags


redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for img_id in col.find({"$and": [
        {"Content-Type.Content": "image/jpeg"},
        {"raw_file": {"$exists": True}}]}, {}):
    job = q.enqueue(insert_yolo_tags, img_id, True)
    print(job.key)

