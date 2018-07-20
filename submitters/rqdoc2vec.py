from rq import Queue
from redis import Redis
import docproc.doc2vec as dv

import pymongo as py
import nltk


# Specify location of nltk_data folder
nltk.data.path.append('/data/nltk_data/')

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

for doc_id in col.find({"content": {"$exists": True} }, {}):
    job = q.enqueue(dv.insert_doc2vec, doc_id)
    print(job.key)


