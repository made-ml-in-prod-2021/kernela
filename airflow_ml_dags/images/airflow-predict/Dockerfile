FROM airflow-ml-base:latest

WORKDIR /home

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./predict.py ./

ENTRYPOINT ["python", "predict.py"]