FROM manifoldai/orbyter-ml-dev
ADD requirements.txt /build/requirements.txt
WORKDIR /build/
RUN pip install --upgrade pip
RUN pip install jupyterlab "ipywidgets>=7.5"
RUN jupyter labextension install jupyterlab-plotly@4.14.3
RUN pip install -r requirements.txt
RUN pip install plotly-geo==1.0.0
RUN jupyter labextension install jupyterlab-dash@0.1.0-alpha.3
WORKDIR /mnt/
