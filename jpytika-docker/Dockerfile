FROM analysis/python-notebook

RUN apt-get -y update
RUN apt-get -y install libreoffice poppler-utils

RUN pip3 --no-cache-dir install tika pdf2image

RUN pip3 install -U pip 
RUN pip3 install -U jupyterlab mayan_api-client rq elasticsearch
RUN pip2 install -U --no-cache-dir supervisor

RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix
#COPY lab/jupyterlab-theme-light-extension/variables.css /usr/local/lib/python3.5/dist-packages/jupyterlab/themes/jupyterlab-theme-light-extension/
#COPY lab/jupyterlab-theme-light-extension/roboto-mono.css /usr/local/lib/python3.5/dist-packages/jupyterlab/themes/jupyterlab-theme-light-extension/

#COPY lab/jupyterlab-theme-dark-extension/variables.css /usr/local/lib/python3.5/dist-packages/jupyterlab/themes/jupyterlab-theme-dark-extension/
#COPY lab/jupyterlab-theme-dark-extension/roboto-mono.css /usr/local/lib/python3.5/dist-packages/jupyterlab/themes/jupyterlab-theme-dark-extension/

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/
