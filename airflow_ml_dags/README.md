# AirFlow и MLFlow

**Данное окружение служит для демострационных целей и не преднозначено для запуска в боевой среде.**

## Требования для запуска

1. Docker 19.04 или выше.
2. docker-compose с поддержкой схемы 3.7 или выше.
3. Из-за особенностей запуска оператооров в Docker необходима ОС на основе Linux или WSL/WSL2 для Windows.
4. В системе предполагается наличие curl для осуществления проверок в сервисах. 

## Как запустить

[Реккомендуется использваоть BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/)

Далее предполагается использование терминала bash.

Выполнить инициализацию СУБД для Airflow:
```
HOST_DATA_DIR="$(pwd)"/data docker-compose run airflow-init
```

В результата должен быть создан пользователь Admin.
```
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.1.0
airflow_ml_dags_airflow-init_1 exited with code 0
```

Собрать образы для DAG:
```
docker-compose -f ./docker-compose.dag.yml build
```

Запустить всё остальное:
```
HOST_DATA_DIR="$(pwd)"/data docker-compose up --build
```

Запуск может происходит с некоторой задержкой т. к. airflow будет инициализировать СУБД, сама СУБД не сразу запуститься и т. п. Везде есть проверки на запуск, но в совсем медленном окружении могут срабоатать проверки на healthcheck и тогда будет ошибка при старте.

По умолчанию после запуска можно открыть след. web-интерфейсы:

1. S3 хранилище Minio [http://localhost:9000/](http://localhost:9000/)
2. Airflow Web UI [http://localhost:8080/](http://localhost:8080/)
3. MLflow Tracking Web UI [http://localhost:5000/](http://localhost:5000/)

Если какие-о порты уже заняты, то их можно поменять в `.env` файле.

Все пароли и логины заданы в переменных окружения смотрите соотв. `docker-compose` и `.env`.

При запуске DSG придётся вручную успешно завершать статусы Sensor т. к. этот функционал не работает судя по обсуждениям, когда DAG запускаются вручную.
