import pymongo as py
import gridfs
import pdf2image
from pytesseract import image_to_string


client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']
fs = gridfs.GridFS(db)


def convert_pdf_to_jpg(i):
    return pdf2image.convert_from_bytes(i, fmt='jpg')


def create_pdf_images(g):
    a = fs.get(g).read()
    img = convert_pdf_to_jpg(a)
    return img


def extract_ocr_text(d):
    return([image_to_string(x) for x in d])


def main():
    pdfs = col.find({"Content-Type": "application/pdf"}, {"raw_file": 1})

    for pdf in pdfs:
        images = create_pdf_images(pdf['raw_file'])
        extracted_text =extract_ocr_text(images)
        print(extracted_text[0])


if __name__ == "__main__":
    main()

