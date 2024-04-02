import copy
import os
from typing import List
from domain.solution import Solution
from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
import matplotlib.pyplot as plt
from utils.plotMaker import PlotMaker
from utils.ADRS import ADRS
import pickle
import numpy as np
from heuristics.heuristic import Heuristic
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","DIGIT"]

class HeuristicSolutions:
    def __init__(self,heuristicName:str,solutionsTimestampsPerBenchmark:dict[list[List[Solution]]]):
        self.heuristicName = heuristicName
        self.solutionsTimestampsPerBenchmark = solutionsTimestampsPerBenchmark

def main():
    graspTimestampsPerBenchmark = {}
    geneticTimestampsPerBenchmark = {} 
    acoTimestampsPerBenchmark = {}
    for benchmark in benchmarks:
        genetic = Graphs.pathToListsOfSolutions(f"../schwarzenegger/savesWithModel/genetic_{benchmark}_2h/")
        grasp  = Graphs.pathToListsOfSolutions(f"../schwarzenegger/savesWithModel/GRASPX_{benchmark}_2h/")
        ACO = Graphs.pathToListsOfSolutions(f"../schwarzenegger/savesWithModel/ACO_{benchmark}_2h/")
        #soft_grasp = Graphs.pathToListsOfSolutions(f"../saves_patati/savesWithModel/SOFT_PRUNING_GRASP_{benchmark}_2h/")
        graspTimestampsPerBenchmark[benchmark] = grasp
        geneticTimestampsPerBenchmark[benchmark] = genetic
        acoTimestampsPerBenchmark[benchmark] = ACO
    solutionsOfAllHeuristics = []    
    solutionsOfAllHeuristics.append(HeuristicSolutions("ACO",acoTimestampsPerBenchmark)) 
    solutionsOfAllHeuristics.append(HeuristicSolutions("GRASP",graspTimestampsPerBenchmark))
    solutionsOfAllHeuristics.append(HeuristicSolutions("GENETIC",geneticTimestampsPerBenchmark))
                                    
    all_heuristics_in_one_bar("PERCENTAGE",solutionsOfAllHeuristics,10)
    all_heuristics_in_one_bar("ADRS",solutionsOfAllHeuristics,10)

def plotHeuristicsComparsion(method:str, solutionsOfAllHeuristics:List[HeuristicSolutions], saveInterval, numberOfTimestamps):
    method = method.upper()
    benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","DIGIT"]
    DEFAULT_LINEWIDTH = 4
    DEFAULT_LINEWIDTH_DECAY = 0.8
    for benchmark in benchmarks:

        numberOfTimestamps = solutionsOfAllHeuristics[0].numberOfTimestamps
        allSolutions = copy.deepcopy(solutionsOfAllHeuristics[0].solutionsTimestampsPerBenchmark[benchmark][numberOfTimestamps-1])
        for i in range(1, len(solutionsOfAllHeuristics)):
            numberOfTimestamps = solutionsOfAllHeuristics[i].numberOfTimestamps
            allSolutions.extend(solutionsOfAllHeuristics[i].solutionsTimestampsPerBenchmark[benchmark][numberOfTimestamps-1])
        
        if method == "PERCENTAGE":
            myplt = PlotMaker(benchmark,'minutes',"Pareto Dominance")
            myplt.ylim(0, 1.1)
            allSolutions = [allSolutions]*solutionsOfAllHeuristics[0].numberOfTimestamps

            comparer = ParetoComparer('resources','latency')
            linewidth=DEFAULT_LINEWIDTH
            for i in range(len(solutionsOfAllHeuristics)):
                Graphs.plotParetoPercentage(myplt,comparer,solutionsOfAllHeuristics[0].solutionsTimestampsPerBenchmark[benchmark],allSolutions,
                                            solutionsOfAllHeuristics[0].heuristicName,saveInterval,linewidth=linewidth)
                linewidth = linewidth*DEFAULT_LINEWIDTH_DECAY

            lns = myplt.lns[0]
            for i in range(len(myplt.lns) -1):
                lns+=myplt.lns[i+1]
            
            labs = [l.get_label() for l in lns]
            myplt.ax.legend(lns, labs, loc=0)
            
        if method == "ADRS":
            myplt = PlotMaker(benchmark,'minutes',"ADRS")

            comparer = ADRS('resources','latency')
            worstADRS = float("-inf")
            for i in range(len(solutionsOfAllHeuristics)):
                adrs = comparer.compare(allSolutions,solutionsOfAllHeuristics[0].solutionsTimestampsPerBenchmark[benchmark])
                if adrs is None:
                    adrs = 0
                if adrs > worstADRS:
                    worstADRS = adrs
            plt.ylim(0,worstADRS + worstADRS/7)

            linewidth=DEFAULT_LINEWIDTH
            for i in range(len(solutionsOfAllHeuristics)):
                Graphs.plotADRS(myplt,comparer,allSolutions,solutionsOfAllHeuristics[0].solutionsTimestampsPerBenchmark[benchmark],
                                solutionsOfAllHeuristics[0].heuristicName,saveInterval,linewidth=linewidth)
                linewidth=DEFAULT_LINEWIDTH_DECAY

            lns = myplt.lns[0]
            for i in range(len(myplt.lns) -1):
                lns+=myplt.lns[i+1]
                
            labs = [l.get_label() for l in lns]
            myplt.ax.legend(lns, labs, loc=0)

        #plt.savefig(f'../schwarzenegger/plotsPNG/{method}/{method}_allHeuristics_{benchmark}.png')
        myplt.showPlot()


def all_heuristics_in_one_bar(method:str, solutionsOfAllHeuristics:List[HeuristicSolutions], numberOfTimestamps):
    method = method.upper()
    benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","DIGIT"]
    myplt = PlotMaker(method,'Heuristics',"Average")
    averages = []

    for benchmark in benchmarks:
        allSolutions = copy.deepcopy(solutionsOfAllHeuristics[0].solutionsTimestampsPerBenchmark[benchmark][numberOfTimestamps-1])
        for i in range(1, len(solutionsOfAllHeuristics)):
            allSolutions.extend(solutionsOfAllHeuristics[i].solutionsTimestampsPerBenchmark[benchmark][numberOfTimestamps-1])
        if method == "PERCENTAGE":
            myplt.ylim(0, 1.1)
            allSolutions = [allSolutions]*10
            for i in range(len(solutionsOfAllHeuristics)):
                averages.append(arithmetic_mean_percentage(solutionsOfAllHeuristics[i].solutionsTimestampsPerBenchmark[benchmark],allSolutions))
            means = []
            #meanGrasp = sum(avgGRASP)/len(avgGRASP)#geometric_mean(avgGRASP)
            #meanGenetic = sum(avgGenetic)/len(avgGenetic)# geometric_mean(avgGenetic)
            #meanSoftGRASP =  sum(avgSoftGRASP)/len(avgSoftGRASP)

        if method == "ADRS":
            pass
            #average ADRS: avg of all best ADRS through time from one heuristic
            #avgACO.append(arithmetic_mean_ADRS(allSolutions,ACO))
            #avgGRASP.append(arithmetic_mean_ADRS(allSolutions,grasp))
            #avgGenetic.append(arithmetic_mean_ADRS(allSolutions,genetic))
            #avgSoftGRASP.append(arithmetic_mean_ADRS(allSolutions,soft_grasp))

            #meanACO = geometric_mean(avgACO)
            #meanGrasp = geometric_mean(avgGRASP)
            #meanGenetic = geometric_mean(avgGenetic)
            #meanSoftGRASP = geometric_mean(avgSoftGRASP)
            
    heuristics = ["SOFT GRASP","GRASP"]
    #maxValue = max(meanSoftGRASP,meanGrasp)
    #plt.ylim(0,maxValue + maxValue/6)
    #myplt.barPlot(heuristics,[meanSoftGRASP,meanGrasp],width=0.6)
    #plt.savefig(f'../schwarzenegger/plotsPNG/{method}/{method}_summarizedBarPlot.png')
    myplt.showPlot()

def geometric_mean(iterable:list):
    a = np.array(iterable)
    lenght = len(a)
    for i in range(lenght):
        if a[i] == 0:
            a = np.delete(a,i)
    return a.prod()**(1.0/len(a))


def arithmetic_mean_ADRS(referenceSet,solutions):
    comparer = ADRS('resources','latency')
    allBestADRS = []
    for i in range(len(solutions)):
        allBestADRS.append(comparer.compare(referenceSet,solutions[i]))
    filtered_items = filter(lambda item: item is not None, allBestADRS)
    new_lst = list(filtered_items)
    return np.mean(new_lst)


def arithmetic_mean_percentage(solutions1,solutions2):
    comparer = ParetoComparer('resources','latency')
    allBestPercentage = []
    for i in range(len(solutions1)):
        allBestPercentage.append(comparer.compare(solutions1[i],solutions2[i]))
    filtered_items = filter(lambda item: item is not None, allBestPercentage)
    new_lst = list(filtered_items)
    return np.mean(new_lst)
main()



#use for adding estimators solutions to heuristics solution
"""
    for benchmark in benchmarks:
        modelFile = f"./models/{benchmark}_MODEL"
        with open(modelFile, "rb") as f:
            model:RandomForestEstimator = pickle.load(f)
        a = model.processor.dataset
        for i in range(10):
            with open(f"../saves_patati/SOFT_PRUNING_GRASP_{benchmark}_2h/timeStampFiller{i}","rb") as heuristicfile:
                b = pickle.load(heuristicfile)
            with open(f"../saves_patati/savesWithModel/SOFT_PRUNING_GRASP_{benchmark}_2h/timeStampFiller{i}","wb") as heuristicfile:
                b.extend(a)
                pickle.dump(b,heuristicfile) 
"""
