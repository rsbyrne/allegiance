#!/bin/bash
MOUNTFROM=$PWD/logs
MOUNTTO='/home/morpheus/workspace/mount/logs'
IMAGE='rsbyrne/allegiance'
SOCK='/var/run/docker.sock'
mkdir logs -p
docker run -v $MOUNTFROM:$MOUNTTO -v $SOCK:$SOCK -it --shm-size 2g --detach-keys 'ctrl-a,a' $IMAGE bash
