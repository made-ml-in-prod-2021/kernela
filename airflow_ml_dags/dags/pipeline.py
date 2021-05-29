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

    data_dir = "/data/raw/{{ ds }}"

    download = DockerOperator(
        image="airflow-download",
        command=f"--out_dir {data_dir}",
        task_id="download-data",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}:/data"]
    )

    eda_anlysis = DockerOperator(image="airflow-eda",
                                 comamnd=f"--report_dir /data/eda/{{ds}} --input_path {data_dir}/data.csv",
                                 task_id="eda",
                                 do_xcom_push=False,
                                 volumes=[f"{HOST_DATA_DIR}:/data"]
                                 )

    split = DockerOperator(image="airflow-split",
                           comamnd=f"--input_dir {data_dir} --input_path /data/raw/{{ ds }}/data.csv",
                           task_id="eda",
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

    download >> eda_anlysis
