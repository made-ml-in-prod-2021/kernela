FROM airflow-ml-base:latest

WORKDIR /home

COPY ./predict.py ./

ENTRYPOINT ["python", "predict.py"]