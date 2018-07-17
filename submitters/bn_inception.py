from rq import Queue
from redis import Redis
import docproc.bottleneck as bn

import pymongo as py



redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for doc_id in col.find({"Content-Type.Content": "application/jpeg"}, {}):
    job = q.enqueue(bn.insert_inception, doc_id)
    print(job.key)