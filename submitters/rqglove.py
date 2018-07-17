from rq import Queue
from redis import Redis
from docproc.docglove import insert_doc2vec

import pymongo as py
import nltk


# Load spacy model
model_path = "/data/spacy/en_core_web_lg"
model = spacy.load(model_path)

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for doc_id in col.find({"content": {"$exists": True} }, {}):
    job = q.enqueue(insert_glove, doc_id)
    print(job.key)


