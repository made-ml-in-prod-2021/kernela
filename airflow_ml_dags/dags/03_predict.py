import os
from datetime import timedelta, datetime

from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.docker.operators.docker import DockerOperator

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

    mlflow_envs = dict()

    for env_name in ("MLFLOW_TRACKING_URL", "MLFLOW_S3_ENDPOINT_URL",
                     "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
        mlflow_envs[env_name] = os.environ[env_name]

    model_name = os.environ["MODEL_NAME"]

    predict = DockerOperator(image="airflow-predict",
                             command="--data_dir /data/raw/{{ ds }} \
                                      --predict_path /data/predictions/{{ ds }}/predictions.csv "
                             f"--model_name  {model_name}",
                             task_id="predict",
                             do_xcom_push=False,
                             auto_remove=True,
                             network_mode="host",
                             private_environment=mlflow_envs,
                             volumes=[f"{HOST_DATA_DIR}:/data"]
                             )

    externalsensor >> predict
