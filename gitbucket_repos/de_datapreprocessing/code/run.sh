#!/bin/bash

set -e

PS4='$ '
set -x

MSG="[>>>>> Set PRORJECT_DIR variable <<<<<]"
export PRORJECT_DIR=$(dirname "$(realpath $0)")

MSG="[>>>>> Set AWS credentials <<<<<]"
set +x
export AWS_ACCESS_KEY_ID=$MINIO_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$MINIO_SECRET_KEY
set -x 


if [ "$DEV_IN_CONTAINER" = "True" ]; then
    MSG="[>>>>> Skip DVC because it is developing in container <<<<<]"

else
    
    MSG="[>>>>> Run tasks in python <<<<<]"
    export GIT_BRANCH=$(if [ $DVC_REMOTE = "local" ]; then echo "main"; else echo $DVC_REMOTE; fi)
    export GIT_REPONAME=de_datapreprocessing
    git clone http://gitbucket:8080/git/root/$GIT_REPONAME.git --branch $GIT_BRANCH $PRORJECT_DIR/cloned_repo
    cd $PRORJECT_DIR/cloned_repo/code
    python main.py

    MSG="[>>>>> List all generated data in the data folder <<<<<]"
    ls -R data

    MSG="[>>>>> Define data version and commit messages <<<<<]"
    export LAST_COMMIT_MSG=$(git log -1 --pretty=%B)
    export DATA_VERSION="CV_$(echo $LAST_COMMIT_MSG | sed 's/ /-/g')_DVC_$(date '+%Y-%m-%d_%H-%M-%S_%Z')"
    export DATA_VERSION_MESSAGE="DVC with version as $DATA_VERSION"
    export tagname=$DATA_VERSION

    MSG="[>>>>> Configure git info and dvc info <<<<<]"
    git config --global user.name airflow
    git config --global user.email "airflow-dev@email.com"

    dvc remote default $DVC_REMOTE

    MSG="[>>>>> Add changes on dvc and git <<<<<]"
    git status
    dvc add data
    git add -A

    MSG="[>>>>> Create git commit and tag <<<<<]"
    git commit -m "$DATA_VERSION_MESSAGE"
    git tag -a "$tagname" -m "$DATA_VERSION_MESSAGE"

    MSG="[>>>>> Git and DVC push <<<<<]"
    git remote set-url origin http://root:root@gitbucket:8080/root/$GIT_REPONAME.git
    git push -u origin --tags 
    dvc push -r $DVC_REMOTE   

fi