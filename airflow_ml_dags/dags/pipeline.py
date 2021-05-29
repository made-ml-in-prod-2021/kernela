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

    report_dir = os.path.join(data_dir, "report")

    eda_anlysis = DockerOperator(image="airflow-eda",
                                 command=f"--report_dir {report_dir} --input_path {data_dir}/data.csv",
                                 task_id="eda",
                                 do_xcom_push=False,
                                 volumes=[f"{HOST_DATA_DIR}:/data"]
                                 )

    train_test_dir = os.path.join(data_dir, "train-test")

    split = DockerOperator(image="airflow-split",
                           command=f"--input_dir {data_dir} --out_dir {train_test_dir}",
                           task_id="split-data",
                           do_xcom_push=False,
                           volumes=[f"{HOST_DATA_DIR}:/data"]
                           )

    model_path = "/data/model/{{ ds }}/model.pickle"

    train = DockerOperator(image="airflow-train",
                           command=f"--train_dir {train_test_dir} --model_path {model_path}",
                           task_id="train",
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

    download >> [eda_anlysis, split]
    split >> train
