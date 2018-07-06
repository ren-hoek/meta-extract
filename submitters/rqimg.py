from rq import Queue
from redis import Redis
from docproc.mgtika import insert_pdf_images
import pymongo as py


redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for pdf_id in col.find({"Content-Type.Content": "application/pdf"}, {}):
    job = q.enqueue(insert_pdf_images, pdf_id)
    print(job.key)

