from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
import matplotlib.pyplot as plt
from utils.plotMaker import PlotMaker
from utils.ADRS import ADRS
import pickle
if __name__ == "__main__": 
    benchmarks =['SHA','AES','GSM','DIGIT']
    heuristics = ['GRASP0','GRASP1','GRASP2','genetic']

    benchmark = 'AES'
    comparer = ParetoComparer('resources','latency')
    benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","OPTICAL","DIGIT"]
    heuristic = 'GRASPX'

    

    for benchmark in benchmarks:
        myplt = PlotMaker(benchmark,'minutes','pareto percentage')
        metrics = ['resources','latency']
        saveInterval = 720
        genetic = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/genetic_{benchmark}_2h/")
        grasp  = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/{heuristic}_{benchmark}_2h/")
        ACO = Graphs.pathToListsOfSolutions(f"../IC_Things/schwarzenegger/savesWithModel/ACO_{benchmark}_2h/")

        adpGRASP = Graphs.averageADP(grasp[0])
        adpGenetic = Graphs.averageADP(ACO[0])
        if adpGenetic == None:
            adpGenetic = 0
        worstADP = max(adpGenetic,adpGRASP)
        #myplt.ylim(0, worstADP + worstADP/2)
        #myplt.ylim(0, 1.1)

        #Graphs.plotParetoPercentage(myplt,comparer,grasp,ACO,heuristic,saveInterval)
        #Graphs.plotParetoPercentage(myplt,comparer,ACO,grasp,'ACO',saveInterval)
        #myplt.twinx()
        #Graphs.plotParetosFrontSize(myplt,grasp,ACO,'size',saveInterval)

        #Graphs.plotADP(myplt,grasp,heuristic,saveInterval)
        #Graphs.plotADP(myplt,ACO,'ACO',saveInterval)
        #myplt.twinx()
        #Graphs.plotAverageADP(myplt,ACO,grasp,'avg',saveInterval)
        
        comparer = ADRS('resources','latency')
        with open(f"./all_solutions/{benchmark}","rb") as solutionsFile:
            allSolutions = pickle.load(solutionsFile)
        Graphs.plotADRS(myplt,comparer,allSolutions,genetic,heuristic,saveInterval)

        plt.savefig(f'../IC_Things/schwarzenegger/plots/ADRS/{benchmark}/ACOXGRASPX')
        myplt.showPlot()


