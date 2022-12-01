from random import sample
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
import pickle
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
from predictor.preprocessing.preProcessor import PreProcessor
from sklearn.model_selection import train_test_split
from predictor.estimators.m5p.m5pEstimator import M5PrimeEstimator
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
    model = M5PrimeEstimator(filesDict['dFile'])
    #heuristic = GRASP(filesDict,'directives.tcl')
    #heuristic = HillClimbing(filesDict,'directives.tcl')
    #heuristic = Greedy(filesDict,'directives.tcl',RESOURCE_TO_COMPARE)
    #heuristic = ExhaustiveSearch(filesDict,'directives.tcl')
    heuristic = RandomSearch(filesDict,'directives.tcl')
    #heuristic = GreedyWithEstimator(filesDict,'directives.tcl')
    #heuristic = RandomSearchWithEstimator(filesDict, 'directives.tcl', model)
    heuristic = GA(filesDict,'directives.tcl',model)
    #heuristic.writeSolutionsDict()
    
    train, test = train_test_split(heuristic.solutions, test_size=0.2, random_state=0)
    model.trainModel(train)
    print(f"SCORE {model.score(test)}")
    paretos = heuristic.paretoSolutions('resources','latency')
    RESOURCE_TO_COMPARE = 'resources'
    ######################### GRAPH
    
    #file para plotar o resultado do computador remoto, caso queira interagir com o plot ao invés de ser só um jpg
    with open('./Plot/solutionsFile', 'wb') as solutionsFile:
        pickle.dump(heuristic, solutionsFile)
    solutionsFile.close()

    plt = PlotMaker("firewall", RESOURCE_TO_COMPARE, 'latency')
    plt.createPlot(heuristic.solutions) #blue
    plt.createPlot(paretos)
    plt.createPlot(heuristic.finalPopulation)
    #paretoPlt = PlotMaker("paretos firewall", RESOURCE_TO_COMPARE, 'latency')
    #samplePLt = PlotMaker("sha", RESOURCE_TO_COMPARE, 'latency')
    #samplePLt.createPlot(heuristic.sample.solutions)
    #plt.createPlot(heuristic.sample2.solutions) #green
    plt.savePlotAsJPG()
    plt.showPlot()
    

    
   
