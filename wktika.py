import os
import io
import tempfile
import requests
from docproc import mayan as my
import pymongo as py
import gridfs
import json
import re
#import tika
from tika import unpack
from pdf2image import convert_from_path
from mayan_api_client import API


def remove_non_ascii(s): return "".join(i for i in s if ord(i)<128)


def get_resp(g, a, s=False):
    """Get Mayan with requests"""
    resp = requests.get(g, auth=a, stream=s)
    if s == False:
        return json.loads(resp.text)
    else:
        return resp


def get_page_num(p):
    """Extract page number from page URL."""
    return p['url'][p['url'].rfind("/")+1:]


def get_next_page(p):
    """Extract p."""
    return p['next'][p['next'].rfind("?")+6:]


def remove_key_periods(d):
    """Recusively remove periods from dictionary.

    Steps through the dictionary and removes and periods
    that are in the keys. Mongo won't accept periods in keys
    as thay are special characters.
    Inputs:
        d: dictionary to step through
    Outputs:
        c: cleansed dictionary.
    """
    c = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = remove_key_periods(v)
        c[k.replace('.', '-')] = v
    return c


def create_bytestream(u, a):
    d = get_resp(u, a, True)
    f = io.BytesIO()
    for chunk in d.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
    f.seek(0)
    return f


def create_temp_file(u, a):
    d = get_resp(u, a, True)
    f = tempfile.NamedTemporaryFile(delete=False)
    for chunk in d.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
    f.seek(0)
    return f

def import_to_gridfs(d, f, n):
    """Import file into gridFS.

    Import an open file into the gridFS of mongo database d.
    Inputs:
        d: Mongo databto import into
        f: File to import
        n: Filename for gridFS
    output:
        b: objectid of imported file
    """
    fs = gridfs.GridFS(d)
    b = fs.put(open(f, 'rb'), filename=n)
    return b


def get_tika_content(d, a):
    """Call TIKA api for rmeta content.

    Calls the rmeta api from TIKA which extracts file metadata
    and content.
    Input:
        d: Mayan document API output
        a: Mayan authorization
    Output:
        c: Dictionary of document metadata and content
    """
    down_url = d['latest_version']['download_url']
    pages = get_resp(d['latest_version']['pages_url'], a)['results']
    try:
        page_no = get_page_num(pages[0])
    except:
        page_no = 0
    f = get_resp(down_url, a, True)
    try:
        c = remove_key_periods(
                unpack.from_buffer(f)
        )
        c['page_no'] = page_no
        c['uuid'] = d['uuid']
        c['checksum'] = d['latest_version']['checksum']
        c['success'] = 1
    except:
        c = dict()
        c['page_no'] = 0
        c['uuid'] = d['uuid']
        c['checksum'] = d['latest_version']['checksum']
        c['success'] = 0
    return (c, f)


def create_pdf_images(p, f):
    """Create images from PDF."""
    return convert_from_path(p + ".pdf", output_folder = f, fmt='jpg')


def import_page_images(d, p, f):
    """Create temporary PDF file."""
    libre_com = (
        "soffice --headless --convert-to pdf:writer_pdf_Export " + p + " --outdir /tmp"
    )
    os.system(libre_com)
    images = create_pdf_images(p, f)
    image_list = [import_to_gridfs(d, f + "/" + n, n) for n in os.listdir(f)]
    return image_list


def clean_temp_files(p, f):
    """Remove temp files and folders.

    Removes the temporary files and folders used in the
    processing.
    Inputs:
        p: Temporary raw file
        f: Folder for temporary images
    """
    for n in os.listdir(f):
        os.remove(f + "/" + n)
    os.rmdir(f)
    os.remove(p)
    os.remove(p + ".pdf")
    return True


def insert_aug_metadata(d, a):
    """Insert TIKA extracted metadata and content."""
    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']

    doc, file_stream = get_tika_content(d, a)

    raw_file = create_temp_file(d['latest_version']['download_url'], a)
    doc['raw_file'] = import_to_gridfs(db, raw_file.name, doc['uuid'])

    temp_dir = tempfile.mkdtemp()
    doc['page_images'] = import_page_images(db, raw_file.name, temp_dir)
    col.insert_one(doc)

    clean_temp_files(raw_file.name, temp_dir)
    return True


auth = (os.environ['MAYAN_USER'], os.environ['MAYAN_PASS'])
mayan = my.MayanAPI()

next_doc = 1
doc_count = 0
doc_content = 0

while next_doc != None:
    all_docs = mayan.documents.documents.get(page=next_doc)
    for doc in all_docs['results']:
        doc_count += 1
        d = insert_aug_metadata(doc, auth)
        print(d)
    if all_docs['next'] != None:
        next_doc = get_next_page(all_docs)
    else:
        next_doc = None

