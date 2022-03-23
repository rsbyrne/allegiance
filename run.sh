#!/bin/bash
MOUNTFROM=$PWD/logs
MOUNTTO='/home/morpheus/workspace/mount/logs'
IMAGE='rsbyrne/allegiance'
SOCK='/var/run/docker.sock'
THREADS=${1:-1000}
TIMEOUT=${2:-3600}
COMMAND=./imrun.sh
mkdir logs -p
docker run -v $MOUNTFROM:$MOUNTTO -v $SOCK:$SOCK --shm-size 2g -d=true $IMAGE $COMMAND $THREADS $TIMEOUT
