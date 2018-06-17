FROM alpine
RUN apk update && apk add --no-cache zlib-dev
RUN pip3 install -U --no-cache-dir pip
RUN pip3 install --no-cache-dir pymongo rq pdf2image
COPY install_tika.py install_tika.py
RUN ./install_tika.py
COPY worker.py worker.py
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
EXPOSE 9998
ENTRYPOINT ["python3", "worker.py"]
