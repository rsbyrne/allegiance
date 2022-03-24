#!/bin/bash
MOUNTFROM=$PWD/logs
MOUNTTO='/allegiance/logs'
IMAGE='rsbyrne/allegiance'
SOCK='/var/run/docker.sock'
COMMAND=./imrun.sh
mkdir logs -p
docker run -v $MOUNTFROM:$MOUNTTO -v $SOCK:$SOCK --shm-size 2g -d=true $IMAGE $COMMAND $@
