# Tutorial

## Deployment 

먼저 deployment.yaml 파일을 디플로이 시킵니다.

```bash 
kubectl apply -f deployment.yaml
```

적용뒤에 라벨을 확인홥니다.

```bash 
kubectl describe deployments.apps nginx-deployment 
k get pods -l app=nginx
```

이후에 replicas 를 1로 변경해준다음에 `kuberctl apply -f deployment.yaml` 실행해서 업데이트 해줍니다.<br>
pods 을 확인해서 1개가 terminating되고 있는지 확인합니다.
