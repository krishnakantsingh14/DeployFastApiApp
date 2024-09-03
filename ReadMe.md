Command to use:
    eval $(minikube docker-env -u)
    kubectl logs <podname> -n namespace
    kubectl describe pod <name>



Demo: 
deployInflux.yaml:
    - NodePort coule be changed to clusterIP (if no data accessed allow from outside)

Bucket: sensordata

For Demo: 
  - Check celery pod logs 


- scale 

rollout undo deployment 
  
