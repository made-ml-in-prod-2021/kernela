# Kubernetes

Весь проект тестировался в minikube 1.20.

## Требования для запуска

1. minikube версии 1.20 или дргуая система, эмулирующая логику Kubernetes.
2. Docker 19.04 или выше при условии запуска minikube с Docker (опционально).

## Запуск pod

Для запуска достаточно запустить minikube с Docker
```
minikube start --driver=docker
```

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
* [online-inference-deployment-rolling-update.yaml](./online-inference-deployment-rolling-update.yaml) deployment приложение со cтратегией обновления когда на кластере одновременно с поднятием новых версии, останаливаются старые

Для удаление различных ресрусов можно воспользоваться командой:
```
minikube kubectl -- delete <resource_type> --all
```