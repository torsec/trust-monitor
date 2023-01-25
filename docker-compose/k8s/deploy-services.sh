#!/bin/bash

# deploy persistent volume for trust monitor logging

kubectl apply -f trust-monitor-storageClass.yaml
kubectl apply -f trust-monitor-persistentVolume.yaml
kubectl apply -f trust-monitor-claim0-persistentvolumeclaim.yaml

# deploy zookeeper and kafka

kubectl apply -f zoo-deployment.yaml
kubectl apply -f zoo-service.yaml
kubectl apply -f kafka-deployment.yaml
kubectl apply -f kafka-service.yaml

# deploy databases
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f mongo-deployment.yaml
kubectl apply -f mongo-service.yaml

# deploy trust monitor

kubectl apply -f trust-monitor-deployment.yaml
kubectl apply -f trust-monitor-service.yaml

# deploy tm GUI

kubectl apply -f tm-gui-deployment.yaml
kubectl apply -f tm-gui-service.yaml
