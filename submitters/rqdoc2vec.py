from rq import Queue
from redis import Redis
from docproc.docvectors import insert_doc2vec

import pymongo as py
import nltk


# Specify location of nltk_data folder
nltk.data.path.append('/data/nltk_data/')

# Specify location of word2vec model
model_path = "/data/GoogleNews-vectors-negative300-SLIM.bin"

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for doc_id in col.find({"content": {"$exists": True} }, {}):
    job = q.enqueue(insert_doc2vec, doc_id, model_path)
    print(job.key)


