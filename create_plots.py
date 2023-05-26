from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
import matplotlib.pyplot as plt
from utils.plotMaker import PlotMaker
from utils.ADRS import ADRS
import pickle
if __name__ == "__main__": 
    benchmarks =['SHA','AES','GSM','DIGIT']
    heuristics = ['GRASP0','GRASP1','GRASP2','genetic']

    heuristic = 'GRASPX'
    benchmark = 'AES'
    comparer = ParetoComparer('resources','latency')
    benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","OPTICAL","DIGIT"]

    


    myplt = PlotMaker(benchmark,'minutes','ADRS')
    metrics = ['resources','latency']
    saveInterval = 720
    genetic = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/genetic_{benchmark}_2h/")
    grasp  = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/{heuristic}_{benchmark}_2h/")
    #adpGRASP = Graphs.averageADP(grasp[0])
    #adpGenetic = Graphs.averageADP(genetic[4])
    #worstADP = max(adpGenetic,adpGRASP)
    #plt.ylim(0, worstADP + worstADP/2)
    #plt.ylim(0, 1.1)
    
    #Graphs.plotParetoPercentage(myplt,comparer,grasp,genetic,heuristic,saveInterval)
    #Graphs.plotParetoPercentage(myplt,comparer,genetic,grasp,'genetic',saveInterval)
    #myplt.twinx()
    #Graphs.plotParetosFrontSize(myplt,grasp,genetic,'size',saveInterval)
    
    #Graphs.plotADP(myplt,grasp,heuristic,saveInterval)
    #Graphs.plotADP(myplt,genetic,'genetic',saveInterval)
    #myplt.twinx()
    #Graphs.plotAverageADP(myplt,genetic,grasp,'avg',saveInterval)
    comparer = ADRS('resources','latency')
    with open(f"./all_solutions/{benchmark}","rb") as solutionsFile:
        allSolutions = pickle.load(solutionsFile)
    grasp = [allSolutions,allSolutions,allSolutions,allSolutions,allSolutions,allSolutions,allSolutions,allSolutions,allSolutions,allSolutions]
    Graphs.plotADRS(myplt,comparer,allSolutions,grasp,heuristic,saveInterval)
    
    #plt.savefig(f'../schwarzenegger/plots/ADRS/justHeuristic/{benchmark}/{heuristic}xgenetic{benchmark}')
    myplt.showPlot()


