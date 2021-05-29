FROM airflow-ml-base:latest

WORKDIR /home

COPY ./download.py ./download.py

ENTRYPOINT [ "python", "./download.py" ] 