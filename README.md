# Metadata Extractor

Project to extract data from a variety of common document types. This data includes: the raw file itself, an image of the file, the text from the file, file metadata, and features for machine learning generated from the file. The data is stored in a NoSQL database and the processing is distributed using job queues.

## Test data
The code as is assumes the test data:
http://downloads.digitalcorpora.org/corpora/files/govdocs1/threads/thread0.zip

has been downloaded and extracted to:
```bash
/data/thread0
```

## Setting up the dockerised app
The main parts of the app consist of the following containers:
* Python environment (including JupyterLab)
* Redis
* MongoDB
* Mongo Express

To build start the containers (which will build the Python environment image if it doesn't exist and pull down the other images from the internet) run
```bash
docker-compose up -d
```
and if the Python environment image needs rebuilding run
```bash
docker-compose up -d --build
```
JupterLab is on port 8888 and the token can be found by typing
```bash
docker logs jpymeta
```
and the Mongo databases can be viewed via Mongo Express on port 8081.

## Example of running a job
To extract text from text documents using Apache Tika and store the results in MongoDB you can run the following commands from within the `jypymeta` container.
First submit the jobs to the queue
```bash
cd meta-extract
python3.5 rqtika.py
```

The Redis job queue can be monitored using
```bash
rq info --url http://redis
```

Next we need to assign workers. The first time you need to create the worker image by building `alpine/rq-tika` image from the `worker-tika` folder. Run
```bash
docker build -t alpine/rq-tika .
```

Then assign *n* workers using the script within the `worker-tika` folder
``bash
./init-rq.sh n
```
and stop them using
```bash
./stop-rq.sh n
```
