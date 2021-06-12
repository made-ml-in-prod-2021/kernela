FROM airflow-ml-base:latest

WORKDIR /home

COPY ./split.py ./

ENTRYPOINT [ "python", "./split.py" ] 