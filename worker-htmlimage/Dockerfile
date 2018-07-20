FROM alpine
RUN apk update && apk add --no-cache gcc g++ gfortran python3-dev musl-dev openblas-dev xorg-server-xephyr xvfb gtk-vnc
RUN apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted qt5-qtbase-dev wkhtmltopdf 
RUN pip3 install -U --no-cache-dir pip
RUN pip3 install --no-cache-dir requests pymongo rq pyvirtualdisplay imgkit
COPY worker.py worker.py
COPY docproc.tar.gz docproc.tar.gz
RUN tar xvzf docproc.tar.gz
RUN rm docproc.tar.gz
EXPOSE 9998
ENTRYPOINT ["python3", "worker.py"]
