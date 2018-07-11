import re
import string
import unicodedata
import numpy as np
import pymongo as py
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from .mgtika import update_doc


def get_wordnet_pos(t):
    """Convert treeback POS tag.

    Converts the tressbank pos tag to wordnet to use
    with the Wordnet lemmatizer

    Input:
        t: treebank pos tag

    Output
        d: wordnet pos tag

    """
    if t.startswith('J'):
        return wordnet.ADJ
    elif t.startswith('V'):
        return wordnet.VERB
    elif t.startswith('N'):
        return wordnet.NOUN
    elif t.startswith('R'):
        return wordnet.ADV
    else:
        return ""


def lemmatize(w, p):
    """Lemmatize word using wordnet.

    Input:
        w: unlemmatized word
        p: pos tag

    Output
        d: lemmatized word

    """
    if p != "":
        return WordNetLemmatizer().lemmatize(w, p)
    else:
        return WordNetLemmatizer().lemmatize(w, wordnet.NOUN)



def word2vec_preprocess(text):
    ''' Preprocess text for use with word2vec model.
    
        Clean the text in the same way as the training data
        used to create the pretrained word2vec model.

        Inputs:
            text: string of text from one document
        Ouput:
            Cleaned list of tokens

    '''
    
    # Remove any whitespace at the start and end of the string
    # and remove any stray tabs and newline characters
    text = text.strip()
    
    # Remove any weird unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
        
    # Convert hyphens and slashes to spaces
    text = re.sub(r'[-/]+',' ',text)
    
    # Remove remaining punctuation
    text = re.sub('['+string.punctuation+']', '', text)
    
    # Convert numbers to text
    text = re.sub(r'0\s*', 'zero ', text)
    text = re.sub(r'1\s*', 'one ', text)
    text = re.sub(r'2\s*', 'two ', text)
    text = re.sub(r'3\s*', 'three ', text)
    text = re.sub(r'4\s*', 'four ', text)
    text = re.sub(r'5\s*', 'five ', text)
    text = re.sub(r'6\s*', 'six ', text)
    text = re.sub(r'7\s*', 'seven ', text)
    text = re.sub(r'8\s*', 'eight ', text)
    text = re.sub(r'9\s*', 'nine ', text)
    
    # Convert the text to lowercase and use nltk tokeniser
    tokens = pos_tag(word_tokenize(text.lower()))
    
    # Lemmatize version and non-lemmatized version
    tokens = [ (lemmatize(x[0], get_wordnet_pos(x[1])), x[0]) for x in tokens]

    # Define a list of stopwords apart from the word 'not'
    stops = set(stopwords.words('english')) - set(('not'))

    # Return un-lemmatized version when lemmatized version not in stops
    return [i[1] for i in tokens if i[0] not in stops]


def normalise(vec):
    '''Normalise a vector.
    
        Input:
            vec: numpy array
        Output:
            Normalised numpy array
    '''
    
    norm = np.linalg.norm(vec)
    if norm < 1e-9:
        return vec
    else:
        return vec / norm

    
def aggregate_wordvecs(tokens, model, dim):
    '''Aggregate word vectors into a document vector.
    
        Simple addition of word vectors to make a document vector
        Inputs:
            tokens: list of cleaned text tokens for a single document
            dim: dimensions of the word vectors
        Output
            Normalised document vector
    '''
    vector = np.zeros(dim)
    for word in tokens:
        if word in model:
            vector += model[word]
               
    return normalise(vector)


def generate_doc2vec(d, model, dim):
    """Generate doc2vec vectors for text.

        Inputs:
            d: text extracted from document
            model: word2vec model
            dim: number of dimensions of word2vec model
        Output:
            vec: feature vectors
    """

    cleaned_tokens = word2vec_preprocess(d)
    vec = aggregate_wordvecs(cleaned_tokens, model, dim)
    vec = normalise(vec)

    return vec


def load_w2v(model_path):
    """Load pre-trained word2vec model

        Inputs:
            model_path: file path of the model to load
        Output:
            model: word2vec model
    """
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    return model
            	

def insert_doc2vec(d, model_path):
    """Insert document vectors.

    Inserts a document vector created from aggregating word2vec vectors.
    Inputs:
        d: Returned ObjectId dictionary from pymongo find
	model_path: path to word vector model
    Output:
        Boolean sucess indictor
    """
    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']

    doc_id = d['_id']
    doc = col.find_one({"_id": doc_id})
    text = doc['content']

    model = load_w2v(model_path) 
    vec = generate_doc2vec(text, model, 300)

    if 'ml-features' not in doc:
        doc['ml-features'] = dict()
    doc['ml-features']['doc2vec'] = vec.tolist()
    success = update_doc(col, doc_id, doc)

    return success

