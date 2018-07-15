from rq import Queue
from redis import Redis
import pymongo as py
from docproc.imgocr import insert_document_ocr_text

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for pdf_id in col.find({"Content-Type.Content": "application/pdf"}, {}):
    #print(insert_document_ocr_text(pdf_id))
    job = q.enqueue(insert_document_ocr_text, pdf_id)
    print(job.key)

