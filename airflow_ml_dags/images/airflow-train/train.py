import click
import os

import mlflow

from log_reg import train

@click.command()
@ click.option("--train_dir")
@ click.option("--exp_name", type=str, required=True)
def mlflow_train(train_dir: str, exp_name: str):
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URL"])

    experiment = mlflow.get_experiment_by_name(exp_name)

    if experiment is None:
        experiment_id = mlflow.create_experiment(exp_name)
        experiment = mlflow.get_experiment(experiment_id)

    mlflow.set_experiment(experiment.name)

    mlflow.sklearn.autolog()

    with mlflow.start_run() as run:
        pipeline = train(train_dir)
        mlflow.sklearn.log_model(sk_model=pipeline,
                                 artifact_path='',
                                 registered_model_name="log_reg")


if __name__ == '__main__':
    mlflow_train()
