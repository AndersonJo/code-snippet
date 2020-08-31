# Tutorial 

## Preparation

 1. 먼저 [Kaggle Fahsion MNIST](https://www.kaggle.com/zalando-research/fashionmnist) 에서 데이터를 다운로드 받습니다.
 

## Postman 설정

 - POST 설정
 - body -> form-data 
    - key: image 
    - key 에서 파일로 변경
    - value: 파일 업로드

## Docker 확인

```bash
docker build -t myapp .
docker run -p 5000:5000 myapp
```

Daemon으로도 실행

```bash
docker run -d -p 5000:5000 --name myapp myapp:latest
```

Postman에서 확인 합니다.

## Docker Hub로 올리기

태그걸어주고 Docker Hub에 올립니다.

```bash
docker tag myapp andersonjo/myapp
docker push andersonjo/myapp
```

## Docker Hub에서 Pull 안하고 Minikube Image 사용하는 방법

```bash
eval $(minikube docker-env)
```

그 다음 build 를 해줍니다.

```bash
docker build -t myapp .
```

Minikube안에서 실행을 합니다. 

```bash
kubectl run myapp-kube --image=myapp:latest --image-pull-policy=Never
```

pods을 확인 하고, Postman에서도 확인합니다.

```bash
kubectl get pods
kubectl port-forward myapp-kube 5000:5000
```

## stateful 로 해보기

아래의 두개의 명령이 되어 있어야 합니다. 

```bash
eval $(minikube docker-env)
docker build -t myapp .
```

배포합니다.

```bash
kubectl apply -f deployment.yaml

kubectl port-forward svc/myapp 5000:80
```

최종적으로 Minikube로 서비스 포트를 열수 있습니다.

```bash
minikube service myapp
```