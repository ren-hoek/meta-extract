import spacy
import numpy as np
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


def fix_bug(model):
    """Fix spacy model bug.

    Spacy english models (version 2.0) do not correctly set
    stop words. This should be fixed in future versions.

    Input:
        model: spacy model
    Output:
        Nothing
    """

    for word in model.Defaults.stop_words:
        lex = model.vocab[word]
        lex.is_stop = True


def glove_preprocess(text):
    """ Preprocess text before aggregation.
    
        Remove stop words, digits and punctuation.

        Inputs:
            text: text object from spacy model
        Ouput:
            Cleaned version of input

    """
    
    processed = []

    for word in text: 
        if word.has_vector and not any([word.is_stop, word.is_digit, word.is_punct]):
            processed.append(word)

    return processed


def normalise(vec):
    """Normalise a vector.
    
        Input:
            vec: numpy array
        Output:
            Normalised numpy array
    """
    
    norm = np.linalg.norm(vec)
    if norm < 1e-9:
        return vec
    else:
        return vec / norm

    
def aggregate_glove(words, model):
    """Aggregate word vectors into a document vector.
    
        Simple average of word vectors to make a document vector
        Inputs:
            words: list of processed spacy words for a single document
        Output
            document vector
    """

    for i, word in enumerate(words):
    	if i==0:
        	combined = word.vector
    	else:
        	combined = np.vstack((combined, word.vector))

    docvector = np.mean(combined, axis=0)
               
    return docvector


def generate_glove(d, model):
    """Generate document vectors for text from glove vectors.

        Inputs:
            d: text extracted from document
            model: spacy model
        Output:
            vec: feature vectors
    """

    doc = model(d.lower())
    processed_words = glove_preprocess(doc)
    vec = aggregate_glove(processed_words, model)

    return vec


def insert_glove(d):
    """Insert document vectors.

    Inserts a document vector created from averaging glove vectors.
    Assumes the spacy model has been imported into this module's namspace
    as "model", to ensure that the model is only loaded once per container.
    Inputs:
        d: Returned ObjectId dictionary from pymongo find
    Output:
        Boolean sucess indictor
    """

    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']

    doc_id = d['_id']
    doc = col.find_one({"_id": doc_id})
    text = doc['content']

    vec = generate_glove(text, model)

    if 'ml-features' not in doc:
        doc['ml-features'] = dict()
    doc['ml-features']['glove'] = vec.tolist()
    success = update_doc(col, doc_id, doc)

    return success

