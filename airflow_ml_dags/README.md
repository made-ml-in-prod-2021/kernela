# AirFlow и MLFlow

## Требования для запуска

1. Docker 19.04 или выше.
2. docker-compose с поддержкой схемы 3.7 или выше.
3. Из-за особенностей запуска оператооров в Docker необходима ОС на основе Linux или WSL/WSL2 для Windows.

## Как запустить

[Реккомендуется использваоть BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/)

Далее предполагается использование терминала bash.

Выполнить инициализацию СУБД для AirFlow:
```
HOST_DATA_DIR="$(pwd)"/data docker-compose up airflow-init
```
