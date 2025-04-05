import time
import logging
import json
import random
import math

import pandas as pd
import numpy as np

from subprocess import Popen, PIPE, call

from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.modelbridge.registry import Models

from k8s_manager import K8sManager
from logfolder_data_source import LogFolderDataSource
from wrk2_log_parser import WrkLogParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler(f"ax-p99-server.log")
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)-10s | %(funcName)-20s || %(message)s',
                              datefmt='%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

HOTELRES_MICROSERVICES = ['consul', 'frontend', 'geo', 'jaeger',
                          'memcached-profile', 'memcached-rate',
                          'memcached-reserve',
                          'mongodb-geo', 'mongodb-profile', 'mongodb-rate',
                          'mongodb-recommendation', 'mongodb-reservation',
                          'mongodb-user', 'profile', 'rate', 'recommendation',
                          'reservation', 'search', 'user']

server_to_ip = {
    "server2.hand32-249629.bayopsys-pg0.wisc.cloudlab.us" : "192.168.1.2",
    "server3.hand32-249629.bayopsys-pg0.wisc.cloudlab.us" : "192.168.1.3",
    "server4.hand32-249629.bayopsys-pg0.wisc.cloudlab.us" : "192.168.1.4",
    "server5.hand32-249629.bayopsys-pg0.wisc.cloudlab.us" : "192.168.1.5",
#    "server6.hand32-213139.bayopsys-pg0.wisc.cloudlab.us" : "192.168.1.6",
#    "server7.hand32-213139.bayopsys-pg0.wisc.cloudlab.us" : "192.168.1.7"
}

def runRemoteCommandGet(com, server):
    #logger.info(f"ssh hand32@{server} {com}")
    p1 = Popen(["ssh", "hand32@"+server, com], stdout=PIPE)
    return p1.communicate()[0].strip()
    
def checkValidParams(params, res, k8sm):
    numAllocs = 0
    arrNodes = []
    for s in HOTELRES_MICROSERVICES:
        k = 'root--'+s
        kn = 'root--'+s+'-node'
        nAlloc = round(params[k])
        nNode = params[kn]
        arrNodes.append(nNode)
        logger.info(f"Scaling {k} to {nAlloc} replicas all running on {nNode}")
        k8sm.scale_deployment_node(name=k, replicas=nAlloc, node=nNode)        
        numAllocs = numAllocs + nAlloc
        
    logger.info(f"Sleeping 120 seconds for the new {numAllocs} allocations to settle.")
    time.sleep(120)
    uniqNodes = set(arrNodes)
    logger.info(f"Unique nodes: {sorted(uniqNodes)}")
    return uniqNodes, numAllocs

def getTotalPwr(uniqNodes):
    totPwr=0.0
    for n in uniqNodes:
        ret = runRemoteCommandGet(f"tail -n 20 ~/perf.{n}.log", server_to_ip[n])
        arrn = []
        for line in str(ret).strip().split("\\n"):
            arrn.append(float(line.strip().split(",")[1]))
        nPwr = np.mean(arrn)
        logger.info(f"{n} {nPwr} W")
        totPwr = totPwr + nPwr
    return totPwr        
    
def evalpeaks(pname, data_source, uniqNodes, params):
    logger.info(f"Sleeping 120 seconds for the hr-client to generate new files.")
    time.sleep(120)
    reward = 999999.0

    ## get data
    data = data_source.get_data()
    if data:
        jdata = json.loads(data["debug"])
        reward = jdata['p99']
        if reward <= 0.0:
            reward = 999999.0
            logger.info(f"BAD reward is {reward}???")
    else:
        logger.info(f"No new P99 data???")
    
    res = {
        pname+"p99": (reward, 0.0),
    }
    logger.info(f"{params} {reward}")
    return res

if __name__ == "__main__":
    k8sm = K8sManager()
    #k8sm.list_pods()
    #res = k8sm.get_cluster_resources()
    res = 128.0
    logger.info(f"k8sm.get_cluster_resources() {k8sm.get_cluster_resources()}")
    #logger.info(f"k8sm.all_pods_running(): {k8sm.all_pods_running()}")
    
    log_parser = WrkLogParser()
    data_source = LogFolderDataSource(log_dir_path="/cilantrologs",
                                      log_parser=log_parser)

    model_kwargs={
        "seed": 999,
        "fallback_to_sample_polytope": True,
    }
    
    gs = GenerationStrategy(
        steps=[
            # 1. Initialization step (does not require pre-existing data and is well-suited for 
            # initial sampling of the search space)
            GenerationStep(
                model=Models.SOBOL,
                num_trials=5,  # How many trials should be produced from this generation step
                min_trials_observed=3, # How many trials need to be completed to move to next model
                max_parallelism=10,  # Max parallelism for this step
                model_kwargs={
                    "seed": 999,
                    "fallback_to_sample_polytope": True,
                },  # Any kwargs you want passed into the model
                model_gen_kwargs={},  # Any kwargs you want passed to `modelbridge.gen`
            ),
            # 2. Bayesian optimization step (requires data obtained from previous phase and learns
            # from all data available at the time of each new candidate generation call)
            GenerationStep(
                model=Models.GPEI,
                num_trials=-1,  # No limitation on how many trials should be produced from this step
                max_parallelism=10,  # Parallelism limit for this step, often lower than for Sobol
                # More on parallelism vs. required samples in BayesOpt:
                # https://ax.dev/docs/bayesopt.html#tradeoff-between-parallelism-and-total-number-of-trials
            ),
        ]
    )
    
    """ setup ax """
    #ax_client = AxClient(generation_strategy=gs, enforce_sequential_optimization=False, verbose_logging=True)
    ax_client = AxClient(generation_strategy=gs, enforce_sequential_optimization=False)
    pname = "peaks"
    params = []
    cons = ""
    for s in HOTELRES_MICROSERVICES:
        d = {}
        d['name'] = "root--"+s
        cons = cons + d['name']+" + "
        d['type'] = "range"
        #d['value_type'] = "float"
        d['value_type'] = "int"
        d['log_scale'] = False
        if 'mongodb' in s:
            d['bounds'] = [1, 2]
        else:
            d['bounds'] = [1, int(res)-len(HOTELRES_MICROSERVICES)-1]
        #d['bounds'] = [1.0, res-len(HOTELRES_MICROSERVICES)-1.0]
        #d['bounds'] = [(1.0/res), (res-len(HOTELRES_MICROSERVICES))/res]
        params.append(d)
    for s in HOTELRES_MICROSERVICES:
        d = {}
        d['name'] = "root--"+s+"-node"
        d['type'] = "choice"
        d['value_type'] = "str"
        d['log_scale'] = False
        d['values'] = k8sm.get_nodes(spec="server")
        params.append(d)
    
    #cons = cons[:-2]+"<= "+str(int(res))
    #consl = cons[:-2]+"<= "+str(res)
    #consh = cons[:-2]+">= "+str(res-1)
    consl = cons[:-2]+"<= "+str(int(res))
    consh = cons[:-2]+">= "+str((int(res)-2))
    #consl = cons[:-2]+"<= 1.0"
    #consh = cons[:-2]+">= 0.98"
    print(consl)
    print(consh)
    
    ax_client.create_experiment(
        name=pname,
        parameters=params,
        objectives={
            pname+"p99": ObjectiveProperties(minimize=True),
        },
        choose_generation_strategy_kwargs={"max_parallelism_override": 40},
        #parameter_constraints=[cons],  # Optional.
        parameter_constraints=[consl, consh],  # Optional.
    )

    #for i in range(0, 1000):
    for i in range(0, 30):
        parameterization, trial_index = ax_client.get_next_trial()
        uniqNodes, numAllocs = checkValidParams(parameterization, res, k8sm)
        """
        if status == False:
            https://github.com/facebook/Ax/issues/372
            difference between abandoning trials and marking them as failed –– when a trial is 'running', it's included in 'pending points' that are passed to the model to indicate that those points should not be re-suggested as they are currently being evaluated. When a trial is 'abandoned', it remains in 'pending points' forever, and when it is marked 'failed', it is removed from pending points. That is because we treat 'failure' as some infrastructural failure during evaluation, which will not necessarily happen again if the same point is re-ran. 'Abandonment', on the other hand, we treat as final decision that a given point should not be part of the experiment.
            rews = {
                pname+"p99": (999999.0, 0.0),
                pname+"pwr": (999999.0, 0.0),
            }
            logger.info(f"This allocation decision is not valid, not all pods are running.")
            ax_client.complete_trial(trial_index=trial_index, raw_data=rews)
        """
        if float(numAllocs) > 132.0:
            rews = {
                pname+"p99": (999999.0, 0.0),
            }
            logger.info(f"Total allocations {numAllocs} is way over the initial budget of {res}, setting a big reward penalty in this case")
            ax_client.complete_trial(trial_index=trial_index, raw_data=rews)
        else:
            ax_client.complete_trial(trial_index=trial_index, raw_data=evalpeaks(pname, data_source, uniqNodes, parameterization))
        ax_client.save_to_json_file("ax-p99-server.json")
        
        #ax_client.abandon_trial(trial_index=trial_index)
        #ax_client.log_trial_failure(trial_index=trial_index)        
    #best_parameters, values = ax_client.get_best_parameters()
    #logger.info(f"ax best_parameters: {best_parameters}")
    #logger.info(f"trace: {ax_client.get_trace()}")
    logger.info(f"**** EXPERIMENT COMPLETE *******")
    
