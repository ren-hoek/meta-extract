from rq import Queue
from redis import Redis
from docproc.mgtika import insert_office_images
import pymongo as py


client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']
i = 0
for doc_id in col.find({"$and": [
        {"Content-Type.Content": "application/msword"},
        {"raw_file": {"$exists": True}}]}, {}):
    job = insert_office_images(doc_id)
    print(job)
