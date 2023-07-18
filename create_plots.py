import copy
from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
import matplotlib.pyplot as plt
from utils.plotMaker import PlotMaker
from utils.ADRS import ADRS
import pickle
import numpy as np
from heuristics.heuristic import Heuristic
method = "PERCENTAGE"


def main():
    for i in range(10,0,-1):
        print(i)
    benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","DIGIT"]
    heuristic = 'GRASPX'
    for benchmark in benchmarks:
        
        saveInterval = 720

        genetic = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/genetic_{benchmark}_2h/")
        grasp  = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/{heuristic}_{benchmark}_2h/")
        ACO = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/ACO_{benchmark}_2h/")
        allSolutions = copy.deepcopy(genetic[9])
        allSolutions.extend(grasp[9])
        allSolutions.extend(ACO[9])

        if method == "PERCENTAGE":
            myplt = PlotMaker(benchmark,'minutes',"Pareto Dominance")
            myplt.ylim(0, 1.1)
            allSolutions = [allSolutions]*10
            comparer = ParetoComparer('resources','latency')
            Graphs.plotParetoPercentage(myplt,comparer,grasp,allSolutions,"GRASP",saveInterval,linewidth=4)
            Graphs.plotParetoPercentage(myplt,comparer,ACO,allSolutions,"ACO",saveInterval,linewidth=2.5)
            Graphs.plotParetoPercentage(myplt,comparer,genetic,allSolutions,"GA",saveInterval,linewidth=1.25)


            lns = myplt.lns[0]
            for i in range(len(myplt.lns) -1):
                lns+=myplt.lns[i+1]
            
            labs = [l.get_label() for l in lns]
            myplt.ax.legend(lns, labs, loc=0)
            
        if method == "ADRS":
            myplt = PlotMaker(benchmark,'minutes',"ADRS")


            comparer = ADRS('resources','latency')
            geneticADRS = comparer.compare(allSolutions,genetic[0])
            GRASPADRS = comparer.compare(allSolutions,grasp[0])
            ACOADRS = comparer.compare(allSolutions,ACO[0])
            if ACOADRS is None:
                ACOADRS = 0
            if GRASPADRS is None:
                GRASPADRS = 0
            if geneticADRS is None:
                geneticADRS = 0
            worstADRS = max(geneticADRS,GRASPADRS,ACOADRS)
            plt.ylim(0,worstADRS + worstADRS/7)
            Graphs.plotADRS(myplt,comparer,allSolutions,grasp,"GRASP",saveInterval,linewidth=4)
            Graphs.plotADRS(myplt,comparer,allSolutions,ACO,"ACO",saveInterval,linewidth=2.5)
            Graphs.plotADRS(myplt,comparer,allSolutions,genetic,"GA",saveInterval,linewidth=1.25)
            lns = myplt.lns[0]
            for i in range(len(myplt.lns) -1):
                lns+=myplt.lns[i+1]
                
            labs = [l.get_label() for l in lns]
            myplt.ax.legend(lns, labs, loc=0)

        plt.savefig(f'../IC_Things/schwarzenegger/plotsPNG/{method}/{method}_allHeuristics_{benchmark}.png')
        myplt.showPlot()


def all_heuristics_in_one_bar():

    benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","DIGIT"]
    heuristic = 'GRASPX'
    myplt = PlotMaker("Pareto Dominance",'Heuristics',"Average")
    avgACO = []
    avgGRASP = []
    avgGenetic = []


    for benchmark in benchmarks:
        genetic = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/genetic_{benchmark}_2h/")
        grasp  = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/{heuristic}_{benchmark}_2h/")
        ACO = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/ACO_{benchmark}_2h/")
        allSolutions = copy.deepcopy(genetic[9])
        allSolutions.extend(grasp[9])
        allSolutions.extend(ACO[9])
        
        if method == "PERCENTAGE":
            myplt.ylim(0, 1.1)
            allSolutions = [allSolutions]*10
            avgACO.append(arithmetic_mean_percentage(ACO,allSolutions))
            avgGRASP.append(arithmetic_mean_percentage(grasp,allSolutions))
            avgGenetic.append(arithmetic_mean_percentage(genetic,allSolutions))
            meanACO = sum(avgACO)/len(avgACO)#geometric_mean(avgACO)
            meanGrasp = sum(avgGRASP)/len(avgGRASP)#geometric_mean(avgGRASP)
            meanGenetic = sum(avgGenetic)/len(avgGenetic)# geometric_mean(avgGenetic)


        if method == "ADRS":
            #average ADRS: avg of all best ADRS through time from one heuristic
            avgACO.append(arithmetic_mean_ADRS(allSolutions,ACO))
            avgGRASP.append(arithmetic_mean_ADRS(allSolutions,grasp))
            avgGenetic.append(arithmetic_mean_ADRS(allSolutions,genetic))


            meanACO = geometric_mean(avgACO)
            meanGrasp = geometric_mean(avgGRASP)
            meanGenetic = geometric_mean(avgGenetic)
            
    heuristics = ["ACO","GRASP","GA"]
    maxValue = max(meanACO,meanGrasp,meanGenetic)
    plt.ylim(0,maxValue + maxValue/6)
    myplt.barPlot(heuristics,[meanACO,meanGrasp,meanGenetic],width=0.6)
    plt.savefig(f'../IC_Things/schwarzenegger/plotsPNG/{method}/{method}_summarizedBarPlot.png')
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
all_heuristics_in_one_bar()





