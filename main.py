from heuristics.impl.GRASP import GRASP
from heuristics.impl.RandomSearch import RandomSearch
from heuristics.impl.greedy import Greedy
from heuristics.heuristic import Heuristic
from heuristics.impl.hillClimbing0 import HillClimbing
from heuristics.impl.exhaustiveSearch import ExhaustiveSearch
from heuristics.impl.greedyWithEstimator import GreedyWithEstimator
from heuristics.impl.randomSearchWithEstimator import RandomSearchWithEstimator
from heuristics.impl.genetic import GA
import argparse
#import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from utils.plotMaker import PlotMaker
import pandas as pd
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
from predictor.estimators.randomforest.randomForestFactory import RandomForestFactory
from predictor.preprocessing.preProcessor import PreProcessor
from sklearn.model_selection import train_test_split
from predictor.estimators.m5p.m5pEstimator import M5PrimeEstimator
from predictor.estimators.m5p.m5pFactory import M5PrimeFactory

if __name__ == "__main__": 
    
    
    #Initialize parser
    parser = argparse.ArgumentParser()
 
    # Adding argument
    parser.add_argument("-c", "--cFiles", help = "C input files list", required=True, nargs='+')
    parser.add_argument("-d", "--dFile", help = "Directives input file",required=True)
    parser.add_argument("-p", "--prjFile", help = "Prj. top file",required=True)
    

 
    # Read arguments from command line
    args = parser.parse_args()
    
    filesDict = {}
    filesDict['cFiles'] = args.cFiles
    filesDict['dFile'] = args.dFile
    filesDict['prjFile'] = args.prjFile

    
    RESOURCE_TO_COMPARE = 'resources'
    model = RandomForestEstimator(filesDict['dFile'])
    #heuristic = HillClimbing(filesDict,'directives.tcl')
    #heuristic = Greedy(filesDict,'directives.tcl',RESOURCE_TO_COMPARE)
    #heuristic = ExhaustiveSearch(filesDict,'directives.tcl')
    #heuristic = RandomSearch(filesDict,'directives.tcl')
    #heuristic = GreedyWithEstimator(filesDict,'directives.tcl')
    #heuristic = RandomSearchWithEstimator(filesDict, 'directives.tcl', model)

    factory = RandomForestFactory(filesDict["dFile"])
    heuristic1 = GA(filesDict,'directives.tcl',factory,5)


    model = RandomForestEstimator(filesDict['dFile'])

    #heuristic2 = GRASP(filesDict,'directives.tcl',model,timeLimit=5,trainTime=1,saveInterval=1500)   
    #file para plotar o resultado do computador remoto, caso queira interagir com o plot ao invés de ser só um jpg
    #heuristic2.writeToFile('./Plot/solutionsFile3')

    #with open("./Plot/solutionsFile",'rb') as file:
    #    heuristic1 = pickle.load(file)
    #with open("./Plot/solutionsFile2",'rb') as file:
    #    heuristic2 = pickle.load(file)
    RESOURCE_TO_COMPARE = 'resources'
    ######################### GRAPH
    plt = PlotMaker("sha", RESOURCE_TO_COMPARE, 'latency')
    plt.createPlot(heuristic1.solutions) #blue
    #plt.createPlot(heuristic2.solutions) 
    '''
    comparer = ParetoComparer(RESOURCE_TO_COMPARE,'latency')
    print(comparer.compare(heuristic1,heuristic2))
    print(comparer.compare(heuristic2,heuristic1))
    '''

    #   plt.createPlot(heuristic.finalPopulation)
    #paretoPlt = PlotMaker("paretos firewall", RESOURCE_TO_COMPARE, 'latency')
    #samplePLt = PlotMaker("sha", RESOURCE_TO_COMPARE, 'latency')
    #samplePLt.createPlot(heuristic.sample.solutions)
    #plt.createPlot(heuristic.sample2.solutions) #green
    plt.savePlotAsJPG()
    plt.showPlot()
    

    
   
