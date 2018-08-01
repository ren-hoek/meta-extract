import os
import glob
from rq import Queue
from redis import Redis
from docproc import catalog as ct
from docproc.mgtika import insert_doc
import pymongo as py

def pass_upload_checks(f):
    """Check file suitable for upload.

    Inputs:
        f: file path
    Output:
        boolean: True if passes all checks
    """
    t = not (
        ct.check_empty_file(f) and
        ct.check_temporary_file(f) and
        ct.check_generic_footer(f) and
        ct.check_file_access_doc(f)
    )
    return t


redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']
file_index = {x['sha1']: True for x in col.find({}, {'_id': 0, 'sha1': 1})}

for file_path in glob.iglob('/data/thread0/*/*'):
    file_hash = ct.create_sha(file_path)
    if file_hash not in file_index:
            file_index[file_hash] = file_path
            file_metadata = ct.create_file_metadata(file_path)
            if pass_upload_checks(file_path):
                job = q.enqueue(insert_doc, file_path, file_hash)
                print(job.key)

