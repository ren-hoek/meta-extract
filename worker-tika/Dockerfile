FROM alpine
RUN apk update && apk add --no-cache zlib-dev jpeg-dev gcc python3-dev musl-dev openjdk7-jre tesseract-ocr poppler-utils
RUN pip3 install -U --no-cache-dir pip
RUN pip3 install --no-cache-dir requests pymongo tika mayan_api-client rq pdf2image pytesseract
COPY install_tika.py install_tika.py
RUN ./install_tika.py
COPY worker.py worker.py
RUN apk update && apk add --no-cache libreoffice ttf-liberation
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
EXPOSE 9998
ENTRYPOINT ["python3", "worker.py"]
