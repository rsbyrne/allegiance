#!/bin/bash
currentDir=$PWD
cd "$(dirname "$0")"
docker build -t rsbyrne/allegiance:latest .
#docker push rsbyrne/allegiance:latest
cd $currentDir
