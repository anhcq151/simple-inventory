#!/bin/bash

set -e

WORKSPACE=/opt/simple-inventory
DEV_IMAGE=localhost/simple-inventory-devcontainer
DATA_VOLUME=simple-inventory-dev
DATA=$WORKSPACE/data
WORKDIR=$(dirname $PWD)
IMAGE_NAME=${WORKDIR##*/}-dev


function run_container()
{
    podman run -d --mount type=volume,source=$1,destination=$2 --volume $3:$4:z --name $1 --publish 8000:5000 $5 /bin/sh -c "while sleep 1000; do :; done"
}


if test -z "$(podman ps --all --format "{{.Image}} {{.Names}}" | grep $DEV_IMAGE)" && test -z "$(buildah images | awk '{print $1}' | grep $DEV_IMAGE)"; then
    echo "No images existed, no container created"
    if test -f Dockerfile; then
        echo "Building dev image..."
        buildah bud --tag $DEV_IMAGE
        echo "Running new container..."
        run_container $DATA_VOLUME $DATA $WORKDIR $WORKSPACE $DEV_IMAGE
    else
        echo "No Dockerfile for building dev container"
        exit 1
    fi
elif test -z "$(podman ps --all --format "{{.Image}} {{.Names}}" | grep $DEV_IMAGE)" && test -n "$(buildah images | awk '{print $1}' | grep $DEV_IMAGE)"; then
    echo "Dev image exists but no dev container is running, creating one..."
    run_container $DATA_VOLUME $DATA $WORKDIR $WORKSPACE $DEV_IMAGE
else
    echo "Dev container is existed and connectable via vscode, nothing to do here!"
fi