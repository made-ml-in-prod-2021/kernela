FROM airflow-ml-base:latest

WORKDIR /home

COPY ./train.py ./train.py

ENTRYPOINT ["python", "train.py"]