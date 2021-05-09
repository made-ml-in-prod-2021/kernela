# homework2

## Требования для запуска

1. Python 3.7 или выше.
2. Docker 19.04 или выше.
3. Git LFS (модели хранятся в LFS).
4. [docker-compose (опционально для упрощения запуска)](https://github.com/docker/compose).

## Как запустить

Для использования BuildKit необходимо установить переменную окружения перед сборкой:
```
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```

### Получение образа

#### Локальная сборка

Собрать образ локально:
```
docker build -t kernela/hear-diss-app:latest .
```

#### Загрузка c Docker Hub

Загрузить [образ с Docker Hub](https://hub.docker.com/repository/docker/kernela/hear-diss-app)

```
docker pull kernela/hear-diss-app:latest
```

### Запуск приложения

#### docker-compose (самый простой вариант)

Выполнить команду:
```
docker-compose up --build
```

Если образ предполагается скачать или он уже скачан, то:
```
docker-compose up
```

### Docker

Для запуска в Docker достаточно выполнить команду:
```
docker run -p 8000:8000 kernela/hear-diss-app:latest
```

В любом случае должно запустится web-приложение. Ожидаемый вывод примерно такой:
```
INFO:     Started server process [8]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

После запуска можно открыть описание API и проверить работу сервиса через web-интерфейс по адресу [http://localhost:8000/docs](http://localhost:8000/docs)

### Запуск скрипта для тестирования сервиса

Установить зависимости:
```
pip install -r ./requirements.txt
```

Для запуска тестового скрипта, который будет делать запросы к сервису и выводить результаты предсказаний выполнить:
```
python ./requester.py --port 8000
```

## Оптимизация образа Docker

1. Выбор подходящего базового образа. Например, образ с Python 3.8-slim весит намного меньше чем другие официальные образы и содержи нужную версию Python.
2. Отключение `cache` для pip. pip по умолчанию кеширует зависимости, чтобы заново не скачивать, но при сборке образа обычно это не нужно.
3. Использование `.dockerignore`. Это аналог `.gitignore`, но для Docker. Позволяет не копировать лишние промежуточные файлы такие как кеши, файлы от тестов и т. п. при копировании целых директорий.
4. Объединение команд в цепочку. Выполнение команду в рамках одной `RUN` инструкции помогает избавиться от лишних слоёв в финальном образе. Особенно, когда создаются промежуточные файлы при выполнении разных команд.

