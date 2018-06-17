import pymongo as py
from docproc import mgtika as mg


client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']


def main():
    pdfs = col.find({"Content-Type.Content": "application/pdf"}, {})

    for pdf in pdfs:
        success = mg.insert_pdf_images(pdf)
        print(success)

        #extracted_text = im.extract_ocr_text(images)
        #print(extracted_text[0])


if __name__ == "__main__":
    main()

