import os
import spacy
import docproc.docglove as dv
from redis import Redis
from rq import Worker, Queue, Connection


# Load the spacy model once per container
model_path = '/data/spacy/en_core_web_lg/en_core_web_lg/en_core_web_lg-2.0.0/'
dv.model = spacy.load(model_path)
dv.fix_bug(dv.model)


listen = ['high', 'default', 'low']


redis_conn = Redis(host='redis')

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
