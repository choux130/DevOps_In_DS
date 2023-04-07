import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'me',
    'description'           : 'DE - Data Preprocessing - Versioned',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 4, 6),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('de_datapreprocessing', 
            default_args=default_args, 
            schedule_interval=None,
            catchup=False) as dag:
    
    t1 = DummyOperator(
        task_id='start'
    )

    t2 = DockerOperator(
        task_id='docker_de_datapreprocessing',
        image=f'{os.environ.get("DOCKERHUB_USR", "")}/de_datapreprocessing:latest',
        api_version='auto',
        auto_remove=True,
        environment={
            "DVC_REMOTE": "master",
            "MYSQL_USR": os.environ.get("MYSQL_USR", ""), 
            "MYSQL_PWD": os.environ.get("MYSQL_PWD", ""),
            "MINIO_ACCESS_KEY": os.environ.get("MINIO_ACCESS_KEY", ""),
            "MINIO_SECRET_KEY": os.environ.get("MINIO_SECRET_KEY", "")
        },
        command="sh run.sh ",
        # command="python main.py",
        docker_url="TCP://docker-socket-proxy:2375",
        docker_conn_id = "dockerhub", 
        network_mode="mynetwork",
        force_pull = True,
        mount_tmp_dir=False, 
        do_xcom_push = False,
    )

    t3 = DummyOperator(
        task_id='end'
    )

    t1 >> t2 >> t3
