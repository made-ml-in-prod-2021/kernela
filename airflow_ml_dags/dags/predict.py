import os
from datetime import timedelta, datetime

from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models.variable import Variable

default_args = {
    "owner": "airflow",
    "retries": 0,
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": True
}

HOST_DATA_DIR = os.environ["HOST_DATA_DIR"]

with DAG(
        dag_id="predict",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=datetime.now()) as dag:

    externalsensor = ExternalTaskSensor(
        task_id="wait-model",
        external_dag_id='prepare-model',
        check_existence=True,
        execution_delta=timedelta(days=1),
        timeout=120)

    predict = DockerOperator(image="airflow-predict",
                             command="--data_dir /data/raw/{{ ds }} \
                                      --predict_path /data/predictions/{{ ds }}/predictions.csv \
                                      --model_path {{ var.value.PROD_MODEL }}",
                             task_id="predict",
                             do_xcom_push=False,
                             volumes=[f"{HOST_DATA_DIR}:/data"]
                             )

    externalsensor >> predict
