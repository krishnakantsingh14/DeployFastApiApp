# Deployment Guide

This guide provides instructions for building Docker images and deploying them using Kubernetes.

## Step 1: Build Docker Images

### Build FastAPI Image

To build the Docker image for FastAPI, use the following command:

```bash
docker build -t fastapi-image:latest .
```

#### Build Celery Worker Image
To build the Docker image for Celery worker, use the following command:
```bash
docker build -t celery-worker:latest .
```


## Step 2: Deploy Using Kubernetes
Apply the following Kubernetes manifests to deploy your application and services:
```bash
kubectl apply -f deployInflux.yaml
kubectl apply -f deployrabbitmq.yaml
kubectl apply -f deployraddis.yaml
kubectl apply -f deployfastapi.yaml
kubectl apply -f deploycelery.yaml
```


### Step 3: Monitoring 


### Things to Consider

#### Commands to Use:

- To switch Docker environment settings to Minikube, use: 

  ```bash
  eval $(minikube docker-env -u)
  ```
- To view logs for a specific pod in a namespace, use:
  ```bash
  kubectl logs <podname> -n namespace
  ```





 
deployInflux.yaml:
    - NodePort coule be changed to clusterIP (if no data accessed allow from outside)
