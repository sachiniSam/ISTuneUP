#!/usr/bin/env python
# coding: utf-8

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
import pandas as pd
import time
import subprocess

#iteration count
count= 1


N_CYCLES = 1


#load the data from configuration file
def loadConfigurations():
    # load data from conf file
    dfConf = pd.read_csv('DeployementConfigs/confData.conf', sep="=", header=None)
    return dfConf

#define the first objeective function to maximize or minimize
def getFirstObjective():
    global firstFitness 
    configData = loadConfigurations()
    firstFitness = configData[configData[0]=='fitnessCriteria1'][1].item()
    if firstFitness == 'minimize':
        firstFitness = -1.0
    else:
        firstFitness = 1.0
    return firstFitness

#define the second objective function to maximize or minimize
def getSecondObjective():
    global secondCriteria
    configData = loadConfigurations()
    secondCriteria = configData[configData[0]=='fitnessCriteria2'][1].item()
    if secondCriteria == 'minimize':
        secondCriteria = -1.0
    else:
        secondCriteria = 1.0
    return secondCriteria

#get the first target objective defined by the user
def getFirstTarget():
    global firstTarMetric
    configData = loadConfigurations()
    firstTarMetric = configData[configData[0]=='targetMetric1'][1].item()
    return firstTarMetric

#get the first target objective defined by the user
def getSecondTarget():
    global secTarMetric
    configData = loadConfigurations()
    secTarMetric = configData[configData[0]=='targetMetric2'][1].item()
    return secTarMetric

#define the populaption size
def definePopulation():
    global populationSize
    configData = loadConfigurations()
    populationSize = int(configData[configData[0]=='population'][1].item())
    return populationSize

#define evolutionary generation
def defineEvolutionaryGen():
    global generationCount
    configData = loadConfigurations()
    generationCount = int(configData[configData[0]=='generation'][1].item())
    return generationCount

#define the optimizer result report path
def setOptimizerResult():
    global optimizerResultPath
    configData = loadConfigurations()
    optimizerResultPath = configData[configData[0]=='overallCsv'][1].item()
    return optimizerResultPath

#load configuration data
dfConf = loadConfigurations()
#load internal configuration parameters
buffer_pool_max = int(dfConf[dfConf[0] == 'buffer_pool_max'][1].item())
log_file_max = int(dfConf[dfConf[0] == 'log_file_max'][1].item())
flush_method_min = dfConf[dfConf[0] == 'flush_method_min'][1].item()
flush_method_max = dfConf[dfConf[0] == 'flush_method_max'][1].item()
thread_cache_max = int(dfConf[dfConf[0] == 'thread_cache_max'][1].item())
thread_sleep_max = int(dfConf[dfConf[0] == 'thread_sleep_max'][1].item())
max_connect_max = int(dfConf[dfConf[0] == 'max_connect_max'][1].item())



#Define how the fitness should be evaluated, as a maximize function
#or as a minimizer function
creator.create("FitnessMax", base.Fitness, weights=(getFirstObjective(),getSecondObjective()))
#Creation of individuals with 
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Possible parameter values with bounds
bufferL, bufferH = 128, buffer_pool_max
logL, logH = 48, log_file_max
flushLH = [flush_method_min,flush_method_max]
cacheL,cacheH = 9, thread_cache_max
sleepL, sleepH = 0, thread_sleep_max
connectionL, connectionH = 151, max_connect_max


#define how each gene will be generated
toolbox.register("attr_bufferPool", random.randint, bufferL, bufferH)
toolbox.register("attr_logFile", random.randint, logL, logH)
toolbox.register("attr_flushMethod", random.choice, flushLH)
toolbox.register("attr_cacheSize", random.randint, cacheL,cacheH)
toolbox.register("attr_sleepDelay", random.randint, sleepL, sleepH)
toolbox.register("attr_MaxConnect", random.randint, connectionL, connectionH)


#build the custome individuals with the registered genes
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_bufferPool,
                  toolbox.attr_logFile,
                  toolbox.attr_flushMethod,
                  toolbox.attr_cacheSize,
                  toolbox.attr_sleepDelay,
                  toolbox.attr_MaxConnect), n=N_CYCLES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    global count
 
    # extract the values of the parameters from the individual chromosome
    bufferP = individual[0]
    logF = individual[1]
    flushM = individual[2]
    cacheS = individual[3]
    sleepD = individual[4]
    maxC = individual[5]

    print(individual)
    
    p = subprocess.Popen(['./MultiObjController.sh',str(int(bufferP)),str(int(logF)),
                      str(flushM),str(int(cacheS)),str(int(sleepD)),
                      str(int(maxC)),str(count)])
    p.wait()
    target1=(pd.read_csv(setOptimizerResult()).iloc[-1][getFirstTarget()])
    target2=(pd.read_csv(setOptimizerResult()).iloc[-1][getSecondTarget()])
    targetResult1 = float(target1)
    targetResult2 = float(target2)
    count = count + 1
    
    return targetResult1, targetResult2


#Custom mutation function for individuals defined,
#during the mutation process , genes will be modified and updaated individuals will be returned
def mutate(individual):
    print("-- Before Mutation--" ,individual)
   
    individual[0] = random.randint(bufferL, bufferH)  
    individual[1] = random.randint(logL, logH)
    if individual[2] == flush_method_min:
        individual[2] = flush_method_max
    else:
        individual[2] = flush_method_min
    individual[3] = random.randint(cacheL,cacheH)
    individual[4] = random.randint(sleepL, sleepH)
    individual[5] = random.randint(connectionL, connectionH)
    

    print("-- After Mutation--" ,individual)
    return individual,


# register the goal / fitness function
toolbox.register("evaluate", evaluate)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator
toolbox.register("mutate", mutate)

# operator for selecting individuals for breeding the next generation
toolbox.register("select", tools.selNSGA2)



def optimize():
    #random.seed(12345)
    # create an initial population
    pop = toolbox.population(n=definePopulation())
    print("population",pop)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.7, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    #fits = [ind.fitness.values[0] for ind in pop]
    fits = [ind.fitness.values for ind in pop]
    print("fits",fits)

    # Variable keeping track of the number of generations
    currentPopulation = 0

    # Begin the evolution
    while currentPopulation < defineEvolutionaryGen():
        # A new generation
        currentPopulation = currentPopulation + 1
        print("-- Generation %i --" % currentPopulation)

        # Select the next generation individuals
        #offspring = toolbox.select(pop, 2)
        parent = toolbox.select(pop, 2)
        # Clone the selected individuals
        ParentCloned = list(map(toolbox.clone, parent))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(ParentCloned[::2], ParentCloned[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in ParentCloned:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in ParentCloned if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("Evaluated %i individuals" % len(invalid_ind))

        # The population is created with offsprinds and selected best parents
        #pop[:] = offspring
        newpop = parent + ParentCloned
        pop[:]= newpop
        
        
        # Gather all the fitnesses in one list and print the stats
        summarizeResult(fits,pop)

    print("-- End of (successful) evolution --")
    multi_best =  toolbox.select(pop, 1)[0]
    print(" MultiObjective Best individual is %s, %s" % (multi_best, multi_best.fitness.values))

    
    

def summarizeResult(fits,pop):
    fits = [ind.fitness.values[0] for ind in pop]

    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)
    std = abs(sum2 / length - mean ** 2) ** 0.5

    print("  Min first Target objective %s" % min(fits))
    print("  Max first Target objective %s" % max(fits))
    print("  Avg first Target objective %s" % mean)
    print("  Std first Target objective %s" % std)

    multi_best =  toolbox.select(pop, 1)[0]
    print(" MultiObjective Best individual is %s, %s" % (multi_best, multi_best.fitness.values))


if __name__ == "__main__":
    optimize()
