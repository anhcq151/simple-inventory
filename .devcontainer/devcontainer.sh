#!/bin/bash

set -e

WORKSPACE=/opt/simple-inventory
DATA=$WORKSPACE/data
DEV_WORKDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROD_WORKDIR=$(cd "$DEV_WORKDIR" && cd .. && pwd)
DEV_IMAGE=${WORKSPACE##*/}-dev
PROD_IMAGE=${WORKSPACE##*/}

function run_dev_container() {
    podman run -d --mount type=volume,source=$1,destination=$2 --volume $PROD_WORKDIR:$4:z --name $1 --publish 5000:5000 $1 /bin/sh -c "while sleep 1000; do :; done"
    podman ps
}

function run_prod_container() {
    podman run -d --mount type=volume,source=$1,destination=$2 --name $1 --publish 8000:5000 $1
    podman ps
}

function is_volume_exist()
{
    if test -z "$(podman volume ls | grep -e "$1$")" 
    then
        echo "Creating new volume..."
        podman volume create $1
    fi
}

function run_container() {

    is_volume_exist $1

    if test -z "$(podman ps --all --format "{{.Names}}" | grep -e "$1$")" && test -z "$(podman images | awk '{print $1}' | grep -e "$1$")"; then
        echo "No images existed, no container created"
        case $1 in
        $DEV_IMAGE)
            if test -f "$3/Dockerfile"; then
                echo "Building dev image..."
                buildah bud -f $3/Dockerfile --tag $1
                echo "Running new dev container..."
                run_dev_container $1 $2 $3 $4
            else
                echo "No Dockerfile for building dev container"
                exit 1
            fi
            ;;
        $PROD_IMAGE)
            if test -f "$PROD_WORKDIR/Dockerfile"; then
                echo "Building app image..."
                buildah bud -f $PROD_WORKDIR/Dockerfile --tag $1
                echo "Running new app container..."
                run_prod_container $1 $2
            else
                echo "No Dockerfile for building app container"
                exit 1
            fi
            ;;
        "")
            echo "Invalid input $1"
            ;;
        esac

    elif test -z "$(podman ps --all --format "{{.Names}}" | grep -e "$1$")" && test -n "$(buildah images | awk '{print $1}' | grep -e "$1$")"; then
        echo "Image exists but no container is running, creating one..."
        case $1 in
        $DEV_IMAGE)
            run_dev_container $1 $2 $3 $4
            ;;
        $PROD_IMAGE)
            run_prod_container $1 $2
            ;;
        "")
            echo "Invalid input $1"
            ;;
        esac

    else
        case $1 in
        $DEV_IMAGE)
            echo "Dev container is existed and connectable via vscode, nothing to do here!"
            ;;
        $PROD_IMAGE)
            echo "App container is existed, starting it now..."
            podman start $1
            ;;
        "")
            echo "Invalid input $1"
            ;;
        esac

    fi
}

choice=$1

case $choice in
dev)
    run_container $DEV_IMAGE $DATA $DEV_WORKDIR $WORKSPACE
    ;;
prod)
    run_container $PROD_IMAGE $DATA
    ;;
"")
    echo "This script requires one positional input: dev | prod"
    ;;
*) echo "Invalid input $1, expected: dev | prod" ;;
esac
