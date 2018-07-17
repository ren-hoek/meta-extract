import os
import nltk
from redis import Redis
import docproc.doc2vec as dv
from rq import Worker, Queue, Connection

# Specify location of nltk_data folder
nltk.data.path.append('/data/nltk_data/')

# Load word2vec model into container so that it is only loaded once
model_path = "/data/GoogleNews-vectors-negative300-SLIM.bin"
dv.model = dv.load_w2v(model_path)

listen = ['high', 'default', 'low']


redis_conn = Redis(host='redis')

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
