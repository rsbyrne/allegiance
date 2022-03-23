#!/bin/bash

REPS=${1:-100}
for i in $(seq $REPS)
do
  python3 ./thread.py ${2:-300} 1> /dev/null 2> /dev/null &
  echo "Launched thread $i"
done
while true
do
  echo "Waiting forever..."
  sleep 3600
done
