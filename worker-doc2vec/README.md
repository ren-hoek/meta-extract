# Notes

This worker creates document vectors by aggregating word2vec vectors for every word. 
These word2vec vectors are obtained from a pre-existing model.

## Prerequisites
This requires that the `nltk` data is stored in `/data/nltk_data`. This can be downloaded using the command:
```bash
sudo python -m nltk.downloader -d /data/nltk_data all
```
where all indicates that all the `nltk` data is to be downloaded, individual items can be specified instead.

Here a cut-down pretrained word2vec model is used from:

https://github.com/eyaler/word2vec-slim

The file `GoogleNews-vectors-negative300-SLIM.bin` needs to be downloaded, uncompressed, and moved to the folder `/data/`. 
```bash
wget https://github.com/eyaler/word2vec-slim/raw/master/GoogleNews-vectors-negative300-SLIM.bin.gz
sudo tar -xvzf GoogleNews-vectors-negative300-SLIM.bin.gz -C /data/GoogleNews-vectors-negative300-SLIM.bin.gz
```

A discussion on the required preprocessing (to ensure the words in your documents match those in the word2vec model) can be found here:

https://groups.google.com/forum/#!topic/word2vec-toolkit/TI-TQC-b53w
