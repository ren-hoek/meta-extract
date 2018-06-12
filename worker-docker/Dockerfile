FROM alpine
RUN apk update && apk add --no-cache libreoffice poppler-utils zlib-dev jpeg-dev gcc python3-dev musl-dev
RUN pip3 install -U --no-cache-dir pip
RUN pip3 install --no-cache-dir requests pymongo tika mayan_api-client rq pdf2image
COPY worker.py worker.py
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz 
ENTRYPOINT ["python3", "worker.py"]
