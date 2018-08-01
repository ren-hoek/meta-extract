from rq import Queue
from redis import Redis
import docproc.bottleneck as bn

import pymongo as py



redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for doc_id in col.find({"metadata.Content-Type": "image/jpeg"}, {}):
    job = q.enqueue(bn.insert_xception, doc_id)
    print(job.key)
