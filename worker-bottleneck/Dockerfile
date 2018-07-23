FROM alpine
RUN apk update && apk add --no-cache gcc g++ gfortran python3-dev musl-dev openblas-dev
RUN pip3 install -U --no-cache-dir pip
RUN apk add --no-cache \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
        hdf5 \
    && apk add --no-cache --virtual .builddeps.edge \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
        hdf5-dev
RUN pip3 install --no-cache-dir requests pymongo rq numpy keras h5py #tqdm
COPY worker.py worker.py
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
EXPOSE 9998
ENTRYPOINT ["python3", "worker.py"]
