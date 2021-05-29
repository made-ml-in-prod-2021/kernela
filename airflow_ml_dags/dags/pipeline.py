import os
from datetime import timedelta, datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "retries": 0
}

HOST_DATA_DIR = os.environ["HOST_DATA_DIR"]

with DAG(
        dag_id="prepare-model",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=datetime.now()) as dag:
    download = DockerOperator(
        image="airflow-download",
        command="--out_dir /data/raw/{{ ds }}",
        task_id="download-data",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}:/data"]
    )

    # preprocess = DockerOperator(
    #     image="mikhailmar/airflow-preprocess",
    #     command="--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}",
    #     task_id="docker-airflow-preprocess",
    #     do_xcom_push=False,
    #     volumes=[
    #         "/Users/mikhail.maryufich/PycharmProjects/airflow_examples/data:/data"]
    # )

    # predict = DockerOperator(
    #     image="mikhailmar/airflow-predict",
    #     command="--input-dir /data/processed/{{ ds }} --output-dir /data/predicted/{{ ds }}",
    #     task_id="docker-airflow-predict",
    #     do_xcom_push=False,
    #     volumes=[
    #         "/Users/mikhail.maryufich/PycharmProjects/airflow_examples/data:/data"]
    # )

    download  # >> preprocess >> predict
