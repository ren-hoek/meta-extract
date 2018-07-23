import numpy as np
from keras.preprocessing import image
from keras.applications import inception_v3, xception, vgg16, resnet50
import h5py as h5py
#from tqdm import tqdm
import pymongo as py


def update_doc(c, i, d, u=False):
    """Update document.

    Update a document within a MongoDB collection.
    Inputs:
        c: MongoDB collection
        i: ObjectId of document to update
        d: Updated document
        u: Create if document doesn't exist
    Output
        Boolean success indicator
    """
    try:
        c.update_one({'_id': i}, {'$set': d}, upsert = u)
        return True
    except:
        return False

    
def get_from_gridfs(d, f):
    """Extract file from gridFS.
    
    Import an open file from the gridFS of mongo database d.
    Inputs:
        d: Mongo db to extract file from
        f: ObjectId of file
    output:
        b: bytestream of file
    """
    fs = gridfs.GridFS(d)
    b = fs.get(f)#.read()
    return b

def read_img(img_id, size):
    """Read and resize image.
    # Arguments
        img_id: string
        size: resize the original image.
    # Returns
        Image as numpy array.
    """
    img = image.load_img(img_id,target_size=size)
    img = image.img_to_array(img)
    return img


def insert_xception(d):
    """Insert xception bottleneck features.
    
    Add instructions
    
    """
    
    POOLING = 'avg'

    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']

    doc_id = d['_id']
    doc = col.find_one({"_id": doc_id})
    grid_id = doc['raw_file']
    
    image = get_from_gridfs(db, grid_id)
    
    img = read_img(image, (299, 299))
    x = inception_v3.preprocess_input(np.expand_dims(img.copy(), axis=0))
        
    inception_bottleneck = inception_v3.InceptionV3(weights='imagenet', include_top=False, pooling=POOLING)
    train_i_bf = inception_bottleneck.predict(x, batch_size=1, verbose=0)

    if 'ml-features' not in doc:
        doc['ml-features'] = dict()
    doc['ml-features']['xception'] = train_i_bf.tolist()
    success = update_doc(col, doc_id, doc)

    return success

