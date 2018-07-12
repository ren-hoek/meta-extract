import os
import spacy


from redis import Redis
from rq import Worker, Queue, Connection


# Specify location of nltk_data folder
mdoel = spacy.load('/data/spacy/en_vectors_web_lg')


listen = ['high', 'default', 'low']


redis_conn = Redis(host='redis')

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
