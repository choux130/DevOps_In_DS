
```sh
docker network create mynetwork
```

```sh
docker compose -f docker-compose-jenkins.yml -p devops up -d

docker compose -f docker-compose-airflow.yml -p airflow up -d
docker compose -f docker-compose-storage.yml -p storage up -d

```


airflow dag repo
```sh
cd ./airflow_dags_repo
git init
git add .
git commit -m "first commit"
git remote add origin http://localhost:8082/git/root/airflow_dags_repo.git
git push -u origin main
```

airflow for git-sync
https://airflow.apache.org/docs/helm-chart/1.4.0/manage-dags-files.html#mounting-dags-from-a-private-github-repo-using-git-sync-sidecar
```sh
ssh-keygen -t rsa -b 4096 -C "admin@email.com"

cat id_rsa|base64 > id_rsa_base64.txt
cat id_rsa|base64.txt --decode           
```
/Users/tingchou/Desktop/DevOps_In_DS/airflow_dags_repo/id_rsa

export GIT_SSH_COMMAND='ssh -i /etc/git-secret/id_rsa'
git clone ssh://root@gitbucket:29418/root/airflow_dags_repo.git

git clone ssh://root@gitbucket:29418/root/airflow_dags_repo.git


https://blog.knoldus.com/how-to-push-a-docker-image-to-docker-hub-using-jenkins/
Jenkins add global credentials for DockerHub

mysql
https://dev.mysql.com/doc/index-other.html
https://downloads.mysql.com/docs/world-setup-en.pdf


References
https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
https://ml-ops.org/content/mlops-principles