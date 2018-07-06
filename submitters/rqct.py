from rq import Queue
from redis import Redis
from docproc.mgtika import insert_content_type
import pymongo as py


redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']


for ct_id in col.find({"metadata.Content-Type": {"$exists": True}}, {}):
    job = q.enqueue(insert_content_type, ct_id)
    print(job.key)

