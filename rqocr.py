from rq import Queue
from redis import Redis
import docproc.mgtika as mg
import pymongo as py
import gridfs
import pytesseract as ts
from PIL import Image

redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

fs = gridfs.GridFS(db)

for pdf_id in col.find({"Content-Type.Content": "application/pdf"}, {}):
    doc = col.find_one({"_id": pdf_id['_id']})
    for x in doc['page_images']:
        print(ts.image_to_string(Image.open(fs.get(x)))
