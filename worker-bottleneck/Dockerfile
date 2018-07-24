FROM ubuntu
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    python3 \
    python3-dev \
    python3-pip \
    libhdf5-dev \
    libatlas-base-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U --no-cache-dir pip
RUN pip3 install --no-cache-dir requests pymongo rq numpy scipy keras h5py tensorflow tqdm
COPY worker.py worker.py
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
EXPOSE 9998
ENTRYPOINT ["python3", "worker.py"]
