import os
from rq import Queue
from redis import Redis
from docproc import mayan as my
from docproc.mytika import insert_aug_metadata, get_next_page
from mayan_api_client import API

auth = (os.environ['MAYAN_USER'], os.environ['MAYAN_PASS'])
mayan = my.MayanAPI()

next_doc = 1

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

while next_doc != None:
    all_docs = mayan.documents.documents.get(page=next_doc)
    for doc in all_docs['results']:
        #insert_aug_metadata(doc, auth)
        job = q.enqueue(insert_aug_metadata, doc, auth)
        print(job.key)
    if all_docs['next'] != None:
        next_doc = get_next_page(all_docs)
        next_doc=None
    else:
        next_doc = None

