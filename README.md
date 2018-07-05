# Metadata Extractor

Project to extract data from a variety of common document types. This data includes: the raw file itself, an image of the file, the text from the file, file metadata, and features for machine learning generated from the file. The data is stored in a NoSQL database and the processing is distributed using job queues.


## Prerequisites

This project assumes you have `docker` and `docker-compose` installed. `docker-compose` can be installed by following the instructions found here:

https://docs.docker.com/compose/install/#install-compose


## Test data
The code as is assumes that the example corpus of documents from:

http://downloads.digitalcorpora.org/corpora/files/govdocs1/threads/thread0.zip

has been downloaded and extracted to the folder 
```bash
/data/thread0
```
on your system.


## Setting up the dockerised app
The main parts of the app consist of the following four containers:
* `jpymeta` – Python environment (including JupyterLab) for submitting jobs to the queue and for writing code to process the documents
* `redis` – Redis database that contains the queue of processing jobs to be run
* `mongo` – MongoDB backend to store the documents and any outputs from the processing jobs
* `mongo-express` – Mongo Express front end which allows you to view the data stored within MongoDB.

To start the containers (which will build the Python environment image if it doesn't exist and pull down the other images from the internet) run
```bash
docker-compose up -d
```
and if the Python environment image needs rebuilding run
```bash
docker-compose up -d --build
```
JupterLab is on localhost port 8888 and the token can be found by typing
```bash
docker logs jpymeta
```
and the Mongo databases can be viewed via Mongo Express on localhost port 8081.

## Example of submitting and running a processing job
The following example extracts text from these documents using Apache Tika and stores the outputs in MongoDB. You can run the following commands from within the `jypymeta` container.

First submit the jobs to the queue
```bash
cd meta-extract
python3.5 rqtika.py
```

The Redis job queue can be monitored using
```bash
rq info --url http://redis
```

Next we need to assign workers to work these jobs. The first time you do this you need to create the worker image by building `alpine/rq-tika` image from the `worker-tika` folder. Run
```bash
docker build -t alpine/rq-tika .
```

Then assign *n* workers using the script within the `worker-tika` folder
```bash
./init-rq.sh n
```
and once the documents have all been processed you can stop the containers using
```bash
./stop-rq.sh n
```
The documents can then be viewed in Mongo Express on local host port 8081.
