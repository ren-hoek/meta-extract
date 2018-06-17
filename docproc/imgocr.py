import os
import io
import uuid
import tempfile
import requests
import pymongo as py
import gridfs
import json
import re
from tika import unpack
from pdf2image import convert_from_path, convert_from_bytes


def remove_non_ascii(s):
    """Remove non-ascii characters."""
    return "".join(i for i in s if ord(i)<128)


def create_uuid():
    """Create random UUID."""
    return str(uuid.uuid4())


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


def get_from_gridfs(d, f):
    """Extract file into gridFS.

    Import an open file into the gridFS of mongo database d.
    Inputs:
        d: Mongo db to extract file from
        f: ObjectId of file
    output:
        b: bytestream of file
    """
    fs = gridfs.GridFS(d)
    b = fs.get(f).read()
    return b


def import_to_gridfs(d, f, n):
    """Import file into gridFS.

    Import an open file into the gridFS of mongo database d.
    Inputs:
        d: Mongo databd to import into
        f: File stream to import
        n: Filename for gridFS
    output:
        b: objectid of imported file
    """
    fs = gridfs.GridFS(d)
    b = fs.put(open(f, 'rb'), filename=n)
    return b


def get_tika_content(f):
    """Call TIKA api for rmeta content.

    Calls the rmeta api from TIKA which extracts file metadata
    and content.
    Input:
        f: file stream
    Output:
        c: Dictionary of document metadata and content
    """
    try:
        c = remove_key_periods(
            unpack.from_file(f)
        )
        c['success'] = 1
    except:
        c = dict()
        c['success'] = 0
    return c


def create_pdf_images(p, f, b=False):
    """Create images from PDF."""
    if b == False:
        return convert_from_path(p + ".pdf", output_folder = f, fmt='jpg')
    else:
        return convert_from_bytes(p, output_folder = f, fmt='jpg')


def clean_temp_files(f, p=''):
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
    if p != '':
        os.remove(p)
        os.remove(p + ".pdf")
    return True


def import_page_images(d, p, f, o=True):
    """Import page images to GridFS.

    Convert and import pages images into GridFS.
    Inputs:
        d: Mongo database
        p: File to convert
        f: Folder to put jpg images
        o: Office file (Boolean)
    Output:
        image_list: List of ObjectIds for GridFS files
    """
    if o == True:
        libre_com = (
            "soffice --headless --convert-to pdf:writer_pdf_Export " + p + " --outdir /tmp"
        )
        os.system(libre_com)
        images = create_pdf_images(p, f)
    else:
        images = create_pdf_images(p, f, True)

    image_list = [import_to_gridfs(d, f + "/" + n, n) for n in os.listdir(f)]
    return image_list


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


def insert_pdf_images(d):
    """Insert TIKA extracted metadata and content."""
    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']

    temp_dir = tempfile.mkdtemp()

    doc_id = d['_id']
    doc = col.find_one({"_id": doc_id})
    pdf_file = get_from_gridfs(db, doc['raw_file'])

    images = import_page_images(db, pdf_file, temp_dir, False)
    doc['page_images'] = images
    col.update_one({'_id': doc_id}, {'$set': doc}, upsert = False)

    clean_temp_files(temp_dir)
    return True

