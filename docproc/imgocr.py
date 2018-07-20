import pytesseract as ts
import pymongo as py
import gridfs
from PIL import Image
from docproc.mgtika import update_doc

def insert_document_ocr_text(d):
    """Insert Tesseract OCR extracted test."""
    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']

    fs = gridfs.GridFS(db)

    doc_id = d['_id']
    doc = col.find_one({"_id": doc_id})
    ocr_text = ""
    for x in doc['page_images']:
        ocr_text += ts.image_to_string(Image.open(fs.get(x)))
    doc['ocr_text'] = ocr_text

    success = update_doc(col, doc_id, doc)
    return success

