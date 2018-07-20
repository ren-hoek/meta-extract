# Notes

This worker creates document vectors by aggregating word2vec vectors for every word.
These glove vectors are obtained from a pre-existing model.

## Prerequisites

This worker requires that the spacy model `en_core_web_lg` is needed to be downloaded and saved in the folder `/data/spacy`,
 for example run these commands:

```bash
sudo mkdir /data/spacy/
wget https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.0.0/en_core_web_lg-2.0.0.tar.gz
sudo tar -xvzf en_core_web_lg-2.0.0.tar.gz -C /data/spacy/
sudo mv en_core_web_lg-2.0.0 en_core_web_lg
```
