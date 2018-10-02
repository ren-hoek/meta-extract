FROM alpine
RUN apk update && apk add --no-cache gcc g++ gfortran python3-dev musl-dev openblas-dev
RUN pip3 install -U --no-cache-dir pip
RUN pip3 install --no-cache-dir requests pymongo rq numpy spacy
COPY worker.py worker.py
COPY rqglove.py rqglove.py
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
EXPOSE 9998
ENTRYPOINT ["python3"]
CMD ["worker.py"]
