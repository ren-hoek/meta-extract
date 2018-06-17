import pymongo as py

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']


def standardize_content_type(c):
    """Standardize content type.

    Inputs:
        c: Content Type
    Output:
        Content Type as a list
    """
    return([x.strip() for x in c.split(";")])


def insert_content_type(d):
    """Insert content type.

    Inserts a standardized content type list in the
    top level of a document.
    Inputs:
        d: Returned ObjectId dictionary from pymongo find
    Output:
        Boolean sucess indictor
    """
    try:
        doc_id = d['_id']
        doc = col.find_one({"_id": doc_id})
        c = doc['metadata']['Content-Type']
        content_type = standardize_content_type(c)
        doc['Content-Type'] = dict()
        doc['Content-Type']['Content'] = content_type[0]
        if len(content_type) == 2:
            doc['Content-Type']['Charset'] = content_type[1]
        col.update_one({'_id': doc_id}, {'$set': doc}, upsert = False)
        return True
    except:
        return False


def main():
    doc_ids = col.find({"metadata.Content-Type": {"$exists": True}}, {})

    for i in doc_ids:
        success = insert_content_type(i)
        print(success)


if __name__ == "__main__":
    main()
