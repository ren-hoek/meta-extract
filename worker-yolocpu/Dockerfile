FROM nvidia/cuda
WORKDIR /
RUN apt-get update -y
RUN apt-get install -y vim gcc make git wget
RUN apt-get -y install libopencv-dev python-opencv
RUN git clone https://github.com/pjreddie/darknet
WORKDIR darknet
COPY Makefile .
RUN make
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN apt-get install -y python-pip
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U rq pymongo
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
COPY rqyolo.py /darknet
COPY worker.py /darknet
ENTRYPOINT ["python"]
CMD ["worker.py"]
