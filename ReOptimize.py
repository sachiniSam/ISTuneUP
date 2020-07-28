#!/usr/bin/env python
# coding: utf-8


from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger

from bayes_opt.event import DEFAULT_EVENTS, Events
from bayes_opt.util import load_logs


import subprocess
import pandas as pd
import time



count= 10


#load the data from configuration file
def loadConfigurations():
    # load data from conf file
    dfConf = pd.read_csv('confData.conf', sep="=", header=None)
    return dfConf

#define the optimization objective
def getObjective():
    global fitnessCriteria 
    configData = loadConfigurations()
    fitnessCriteria = configData[configData[0]=='fitnessCriteria'][1].item()
    if fitnessCriteria == 'minimize':
        fitnessCriteria = -1
    else:
        fitnessCriteria = 1
    return fitnessCriteria

#get the target objective defined by the user
def getTarget():
    global targetMetric
    configData = loadConfigurations()
    targetMetric = configData[configData[0]=='targetMetric'][1].item()
    return targetMetric

#define the optimizer result report path
def setOptimizerResult():
    global optimizerResultPath
    configData = loadConfigurations()
    optimizerResultPath = configData[configData[0]=='resultData'][1].item()
    return optimizerResultPath

#define the logger path
def setLoggerRoute():
    global loggerRoute
    configData = loadConfigurations()
    loggerRoute = configData[configData[0]=='loggerPath'][1].item()
    return loggerRoute

#define the  iterations for the optimizer
def defineOptIterations():
    global iterations
    configData = loadConfigurations()
    iterations = int(configData[configData[0]=='iterations'][1].item())
    return iterations



# load data from conf file
dfConf = pd.read_csv('confData.conf', sep="=", header=None)
buffer_pool_max = dfConf[dfConf[0] == 'buffer_pool_max'][1].item()
log_file_max = dfConf[dfConf[0] == 'log_file_max'][1].item()
flush_method_max = dfConf[dfConf[0] == 'flush_method_max'][1].item()
thread_cache_max = dfConf[dfConf[0] == 'thread_cache_max'][1].item()
thread_sleep_max = dfConf[dfConf[0] == 'thread_sleep_max'][1].item()
max_connect_max = dfConf[dfConf[0] == 'max_connect_max'][1].item()


def objFunction(buffer_pool,log_file,flush_method,thread_cache,thread_sleep,max_connect):
    global count
    
    p = subprocess.Popen(['./BayesController.sh',str(int(buffer_pool)),str(int(log_file)),
                     str(int(flush_method)),str(int(thread_cache)),str(int(thread_sleep)),
                     str(int(max_connect)),str(count)])
    p.wait()
    latc=(pd.read_csv(setOptimizerResult()).iloc[-1][getTarget()])
    latency=getObjective()*float(latc)
    count = count + 1
    
    
    return latency


# Bounded region of parameter space
pbounds = {'buffer_pool': (128, buffer_pool_max), 'log_file': (48, log_file_max),'flush_method': (0, flush_method_max),
           'thread_cache': (9, thread_cache_max),'thread_sleep': (0, thread_sleep_max), 'max_connect': (151, max_connect_max)}

optimizer = BayesianOptimization(
    f=objFunction,
    pbounds=pbounds,
    random_state=1,
)



load_logs(optimizer, logs=[setLoggerRoute()])
logger = JSONLogger(path="./logsResumed.json")

optimizer.subscribe(Events.OPTMIZATION_STEP, logger)



print("New optimizer is now aware of {} points.".format(len(optimizer.space)))
count=len(optimizer.space)

optimizer.maximize(
    init_points=0,
    n_iter=defineOptIterations(),
)

print(optimizer.max)

#combine the final json files
f2data = "" 
with open('./logsResumed.json') as f2: 
  f2data = '\n' + f2.read()    
with open(setLoggerRoute(),'a+') as f1:
    f1.write(f2data)

