from rq import Queue
from redis import Redis
from docproc.htmlimage import insert_html_images

import pymongo as py


redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for doc_id in col.find({"$and": [
        {"Content-Type.Content": "text/html"},
        {"raw_file": {"$exists": True}}]}, {}):
    job = q.enqueue(insert_html_images, doc_id)
    print(job.key)
