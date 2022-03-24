#!/bin/bash
service tor start
# echo $(curl --socks5 127.0.0.1:9050 https://check.torproject.org |& grep -Po "(?<=strong>)[\d\.]+(?=</strong)")
MODE=${1:-cycle}
shift 1
python3 ./slowloris.py $MODE $@ #1> /dev/null 2> /dev/null
