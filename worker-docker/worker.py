import os

from redis import Redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']


redis_conn = Redis(host='redis')

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
