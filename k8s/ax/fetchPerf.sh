#!/bin/bash

#set -x

export NITERS=${NITERS:=2}
export WORKERS=${WORKERS:="192.168.1.2 192.168.1.3 192.168.1.4 192.168.1.5"}
export SCHED=${SCHED:="performance"}

mkdir -p $SCHED/results

for w in $WORKERS; do
    ssh $w "nohup perf stat -a -e power/energy-pkg/ -x, -I 1000 sleep $((NITERS*3600)) > perf.log 2>&1 &"
done

for ((t=0;t<$NITERS;t++)); do
    kubectl cp $(kubectl get pods | awk '/hr-client/ {print $1;exit}'):/cilantrologs $SCHED/results/cilantrologs
    kubectl cp $(kubectl get pods | awk '/hr-client/ {print $1;exit}'):/nohup.out $SCHED/results/nohup.out
    kubectl cp -c ax-server $(kubectl get pods | awk '/hr-client/ {print $1;exit}'):/peakler/kapi/peaks $SCHED/results/peaks

    kubectl get pods -o wide > $SCHED/results/kubectl.pods.$t
    kubectl get pods -o wide --all-namespaces > $SCHED/results/kubectl-all-namespaces.pods.$t

    for w in $WORKERS; do
	scp -r $w:~/perf.log $SCHED/results/perf.$w.log
    done

    echo "Sleeping 3600s ......"
    sleep 3600
done

#./clean_cluster.sh
