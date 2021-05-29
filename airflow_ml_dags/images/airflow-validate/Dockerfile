FROM airflow-ml-base:latest

WORKDIR /home

COPY ./validate.py ./

ENTRYPOINT ["python", "validate.py"]