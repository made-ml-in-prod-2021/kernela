FROM airflow-ml-base:latest

WORKDIR /home

COPY ./requiremnets.txt ./

RUN pip install --no-cache -r ./requiremnets.txt

COPY ./train.py ./log_reg.py ./

ENTRYPOINT ["python", "train.py"]