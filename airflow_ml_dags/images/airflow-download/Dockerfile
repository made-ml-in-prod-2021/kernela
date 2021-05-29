FROM airflow-ml-base:latest

WORKDIR /home

COPY ./download.py ./

ENTRYPOINT [ "python", "./download.py" ] 