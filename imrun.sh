#!/bin/bash

REPS=${1:-100}
service tor start
python3 ./attack.py ${2:-300} 1> /dev/null 2> /dev/null &

# for i in $(seq $REPS)
# do
#   python3 ./thread.py ${2:-300} 1> /dev/null 2> /dev/null &
#   echo "Launched thread $i"
# done
# while true
# do
#   echo "Waiting forever..."
#   sleep 3600
# done
