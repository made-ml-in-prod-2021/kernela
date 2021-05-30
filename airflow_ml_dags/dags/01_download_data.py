import os
from datetime import timedelta, datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "retries": 0,
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": True,
}

HOST_DATA_DIR = os.environ["HOST_DATA_DIR"]

with DAG(
        dag_id="data-extractor",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=datetime.now()) as dag:

    data_dir = "/data/raw/{{ ds }}"

    download = DockerOperator(
        image="airflow-download",
        auto_remove=True,
        command=f"--out_dir {data_dir}",
        task_id="download-data",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}:/data"]
    )

    download
