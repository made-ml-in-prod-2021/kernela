# Kubernetes

Весь проект тестировался в minikube 1.20.

## Требования для запуска

1. minikube версии 1.20 или дргуая система, эмулирующая логику Kubernetes.
2. Docker 19.04 или выше при условии запуска minikube с Docker (опционально).
3. [Helm версии 3 для запуска helm package.](https://helm.sh/docs/intro/install/)

**Все команды приведены для minikube. При наличии других систем точный синтаксис может отличаться. Например, не нужно везде писать `minikube`** 

## Запуск кластера

Для запуска достаточно запустить minikube с Docker
```
minikube start --driver=docker
```

## Запуск pod

После старта достаточно выполнить команду:
```
minikube kubectl -- apply -f ./file_name.yaml
```
где `file_name.yaml`:

* [online-inference-pod.yaml](./online-inference-pod.yaml) простой pod manifests
* [online-inference-pod-resources.yaml](./online-inference-pod-resources.yaml) простой pod manifests с указанием ресурсов
* [online-inference-pod-probes.yam](./online-inference-pod-probes.yaml) pod с падающим приложением через некоторое время после запуска
* [online-inference-replicaset.yaml](./online-inference-replicaset.yaml) запуск нескольких instance приложений
* [online-inference-deployment-blue-green.yaml](./online-inference-deployment-blue-green.yaml) deployment приложение со cтратегией обновления когда на кластере есть как все старые поды, так и все новые
* [online-inference-deployment-rolling-update.yaml](./online-inference-deployment-rolling-update.yaml) deployment приложение со cтратегией обновления когда на кластере одновременно с поднятием новых версии, останавливаются старые

Для удаление различных ресурсов можно воспользоваться командой:
```
minikube kubectl -- delete <resource_type> --all
```

## Запуск через Helm

Выполнить команду:
```
helm install web-deploy ./diss-app-web-chart
```

Посмотреть статус:
```
helm status web-deploy
```

Вывод должен быть примерно таким:
```
NAME: web-deploy
LAST DEPLOYED: Sun Jun 13 13:22:03 2021
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
```

Выполнить команду:
```
minikube kubectl -- get svc
```

Необходимо найти NodePort, принадлежащий только что развёрнотому сервису. Его имя будет начинаться с `web-deploy`. Например:
```
web-deploy-diss-app-web   NodePort    10.111.93.14   <none>        8000:31709/TCP   14m
```

Выполнить команду для доступа к сервису:
```
minikube service --url web-deploy-diss-app-web
```

Должен сгенерироваться URL для доступа к сервису. Например:
```
|-----------|--------------------------|-------------|------------------------|
| NAMESPACE |           NAME           | TARGET PORT |          URL           |
|-----------|--------------------------|-------------|------------------------|
| default   | test-deploy-diss-app-web |             | http://127.0.0.1:39191 |
|-----------|--------------------------|-------------|------------------------|
http://127.0.0.1:39191
```

Его достаточно скопировать в адресную строку браузера и добавить путь `/docs`:
```
http://127.0.0.1:39191/docs
``` 

После этого должна открыться страница с описанием API сервиса.