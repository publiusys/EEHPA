#!/bin/bash

set -x

export NITERS=${NITERS:=20}
export WORKERS=${WORKERS:="192.168.1.2 192.168.1.3 192.168.1.4 192.168.1.5 192.168.1.6"}

## run 20 hrs
for w in $WORKERS; do
    ssh $w "nohup perf stat -a -e power/energy-pkg/ -x, -I 1000 sleep $((NITERS*3600)) > perf.log 2>&1 &"
done
