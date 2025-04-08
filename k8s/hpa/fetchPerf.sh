#!/bin/bash

#set -x

export NITERS=${NITERS:=3}
export WORKERS=${WORKERS:="192.168.1.2 192.168.1.3 192.168.1.5"}
export SCHED=${SCHED:="performance"}

mkdir -p $SCHED/results

for w in $WORKERS; do
    ssh $w "nohup perf stat -a -e power/energy-pkg/ -x, -I 1000 sleep $((NITERS*3600)) > perf.log 2>&1 &"
done

# pre-fetch
kubectl logs $(kubectl get pods | awk '/dsb/ {print $1;exit}') > $SCHED/results/dsb.log
kubectl cp $(kubectl get pods | awk '/dsb/ {print $1;exit}'):/nohup.out $SCHED/results/nohup.out
kubectl cp $(kubectl get pods | awk '/dsb/ {print $1;exit}'):/cilantrologs $SCHED/results/cilantrologs

kubectl get pods -o wide > $SCHED/results/kubectl.pods.0
kubectl get pods -o wide --all-namespaces > $SCHED/results/kubectl-all-namespaces.pods.0
kubectl get hpa > $SCHED/results/kubectl.hpa.0

for w in $WORKERS; do
    scp -r $w:~/perf.log $SCHED/results/perf.$w.log
done
    
for ((t=0;t<$NITERS;t++)); do
    echo "Sleeping......"
    sleep 3600
    
    kubectl logs $(kubectl get pods | awk '/dsb/ {print $1;exit}') > $SCHED/results/dsb.log
    kubectl cp $(kubectl get pods | awk '/dsb/ {print $1;exit}'):/nohup.out $SCHED/results/nohup.out
    kubectl cp $(kubectl get pods | awk '/dsb/ {print $1;exit}'):/cilantrologs $SCHED/results/cilantrologs

    kubectl get pods -o wide > $SCHED/results/kubectl.pods.$t
    kubectl get pods -o wide --all-namespaces > $SCHED/results/kubectl-all-namespaces.pods.$t
    kubectl get hpa > $SCHED/results/kubectl.hpa.$t
    
    for w in $WORKERS; do
    	scp -r $w:~/perf.log $SCHED/results/perf.$w.log
    done
done

#./clean_cluster.sh
