import os
from datetime import timedelta, datetime

from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
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
        dag_id="prepare-model",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=datetime.now()) as dag:

    data_dir = "/data/raw/{{ ds }}"
    
    externalsensor = FileSensor(
        task_id="airflow-wait-file",
        filepath="raw/{{ ds }}",
        fs_conn_id="data_path"
    )

    report_dir = os.path.join(data_dir, "report")

    eda_anlysis = DockerOperator(image="airflow-eda",
                                 command=f"--report_dir {report_dir} --input_path {data_dir}/data.csv",
                                 task_id="eda",
                                 do_xcom_push=False,
                                 auto_remove=True,
                                 volumes=[f"{HOST_DATA_DIR}:/data"]
                                 )

    train_test_dir = os.path.join(data_dir, "train-test")

    split = DockerOperator(image="airflow-split",
                           command=f"--input_dir {data_dir} --out_dir {train_test_dir}",
                           task_id="split-data",
                           do_xcom_push=False,
                           auto_remove=True,
                           volumes=[f"{HOST_DATA_DIR}:/data"]
                           )

    mlflow_envs = dict()

    for env_name in ("MLFLOW_TRACKING_URL", "MLFLOW_S3_ENDPOINT_URL", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
        mlflow_envs[env_name] = os.environ[env_name]

    model_name = os.environ["MODEL_NAME"]

    train = DockerOperator(image="airflow-train",
                           command=f"--train_dir {train_test_dir}/train --exp_name train-exp --model_name {model_name}",
                           task_id="train",
                           do_xcom_push=False,
                           auto_remove=True,
                           network_mode="host",
                           private_environment=mlflow_envs,
                           volumes=[f"{HOST_DATA_DIR}:/data"]
                           )

    validate = DockerOperator(image="airflow-validate",
                              command=f"--valid_dir {train_test_dir}/test --model_name {model_name} --exp_name {model_name}-validate",
                              task_id="validate",
                              do_xcom_push=False,
                              auto_remove=True,
                              network_mode="host",
                              private_environment=mlflow_envs,
                              volumes=[f"{HOST_DATA_DIR}:/data"]
                              )

    externalsensor >> [eda_anlysis, split]
    split >> train >> validate
