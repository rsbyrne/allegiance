#!/bin/bash
echo $(curl --socks5 127.0.0.1:9050 https://check.torproject.org |& grep -Po "(?<=strong>)[\d\.]+(?=</strong)")
