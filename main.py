from ast import arguments, dump
from distutils.errors import PreprocessError
from pickle import TRUE
from random import sample
from re import X
from setuptools import Require
from GRASP import GRASP
from RandomSearch import RandomSearch
from greedy import Greedy
from heuristic import Heuristic
from hillClimbing0 import HillClimbing
from exhaustiveSearch import ExhaustiveSearch
from greedyWithEstimator import GreedyWithEstimator
from randomSearchWithEstimator import RandomSearchWithEstimator
from genetic import GA
import argparse
#import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from plotMaker import PlotMaker
import pandas as pd
import pickle
from randomForest import RandomForestEstimator
from preProcessor import PreProcessor
from sklearn.model_selection import train_test_split
from m5pEstimator import M5PrimeEstimator
if __name__ == "__main__":
    
    
    #Initialize parser
    parser = argparse.ArgumentParser()
 
    # Adding argument
    parser.add_argument("-c", "--cFiles", help = "C input files list", required=TRUE, nargs='+')
    parser.add_argument("-d", "--dFile", help = "Directives input file",required=TRUE)
    parser.add_argument("-p", "--prjFile", help = "Prj. top file",required=TRUE)

 
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
    #heuristic = RandomSearch(filesDict,'directives.tcl')
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
    
    
    ######################### GRAPH
    
    # hText = 0.8
    # for solution in heuristic.solutions:
    #     plt.figtext(0.05, hText,solution, fontsize=9)
    #     plt.figtext(0.05 , hText-0.05, 'Latency:', fontsize=8)
    #     plt.figtext(0.15 , hText-0.05, listLat[solution-1], fontsize=8)
    #     plt.figtext(0.05 , hText-0.1, '#LUT:', fontsize=8)
    #     plt.figtext(0.15 , hText-0.1, listLUT[solution-1], fontsize=8)
    #     hText -= 0.15  


    
   
