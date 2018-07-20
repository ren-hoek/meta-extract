FROM ubuntu:16.04

USER root

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget vim tmux curl git \
    bzip2 ca-certificates sudo locales \
    fonts-liberation gdebi-core \
    build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev \
    libzmq3-dev libsasl2-dev libgsl0-dev libudunits2-dev \
    libprotobuf-dev libgdal-dev openjdk-8-jdk \
    libmagick++-dev libglu1-mesa-dev libffi-dev libgsl-dev \
    libv8-3.14-dev libproj-dev libreoffice poppler-utils \
    python3 python3-dev python3-pip enchant python python-dev python-pip \
    python3-tk python-tk xvfb xserver-xephyr vnc4server wkhtmltopdf tesseract-ocr
RUN apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.10.0/tini && \
    echo "1361527f39190a7338a0b434bd8c88ff7233ce7b9a4876f3315c22fce7eca1b0 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

RUN apt-get install -y python-setuptools python3-setuptools
RUN apt-get clean

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -U notebook jupyterhub jupyterlab virtualenv
RUN jupyter serverextension enable --py jupyterlab --sys-prefix

RUN virtualenv py27 --python=python2.7
RUN . /py27/bin/activate; pip install --no-cache-dir -U ipykernel
RUN . /py27/bin/activate; python -m ipykernel install --name py27 --display-name "Python 2.7"

ADD requirements.txt /tmp/python/
RUN pip3 install --no-cache-dir -U -r /tmp/python/requirements.txt
RUN . /py27/bin/activate; pip install --no-cache-dir -U -r /tmp/python/requirements.txt

RUN apt-get -y update
RUN apt-get -y install python3-tk python-tk

RUN python3 -m spacy download en
RUN . /py27/bin/activate; python -m spacy download en

RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "--"]
CMD ["start-notebook.sh"]
