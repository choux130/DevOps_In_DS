

# start the dvc 
```sh
dvc init
```

edit the dvc config file
```sh
['remote "local"']
    url = s3://local-01-data-preprocessing/dvc
    endpointurl = http://minio:9000
['remote "master"']
    url = s3://master-01-data-preprocessing/dvc
```


get data
```sh
dvc get http://gitbucket:8080/git/root/01_data_preprocessing.git code/data --rev DVC_2023-04-05_16-21-31_UTC+0000 
```