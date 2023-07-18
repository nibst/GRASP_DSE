import argparse
import json
import pickle

import pandas as pd
#import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from sklearn.model_selection import train_test_split

from heuristics.heuristic import Heuristic
from heuristics.impl.antColony import AntColony
from heuristics.impl.exhaustiveSearch import ExhaustiveSearch
from heuristics.impl.genetic import GA
from heuristics.impl.GRASP import GRASP
from heuristics.impl.greedy import Greedy
from heuristics.impl.greedyWithEstimator import GreedyWithEstimator
from heuristics.impl.hillClimbing0 import HillClimbing
from heuristics.impl.RandomSearch import RandomSearch
from heuristics.impl.randomSearchWithEstimator import RandomSearchWithEstimator
from predictor.estimators.m5p.m5pEstimator import M5PrimeEstimator
from predictor.estimators.m5p.m5pFactory import M5PrimeFactory
from predictor.estimators.randomforest.randomForest import \
    RandomForestEstimator
from predictor.estimators.randomforest.randomForestFactory import \
    RandomForestFactory
from predictor.preprocessing.preProcessor import PreProcessor
from utils.estimatorTrainer import RandomSamplesEstimatorTrainer
from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
from utils.plotMaker import PlotMaker
from utils.timeLapsedSolutionsSaver import TimeLapsedSolutionsSaver

if __name__ == "__main__": 
   
    parser = argparse.ArgumentParser()
    with open('./benchmarks.json') as jsonFile:
        benchmarks:dict =  json.load(jsonFile)
    benchmarksList = list(benchmarks.keys())
    # Adding argument
    #only one of the two arguments in 'group' are required
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-b", "--benchmark", help = "Which benchmark",choices=benchmarksList)
    group.add_argument("-c", "--cFiles", help = "C input files list", nargs='+')

    parser.add_argument('heuristic')
    parser.add_argument("-d", "--dFile", help = "Directives input file",required=False)
    parser.add_argument("-p", "--prjFile", help = "Prj. top file",required=False)

    parser.add_argument("-o", "--saveFile", help = "name of save file",required=True)
    parser.add_argument("-model", "--estimationModel", help = "model used in heuristics for estimation of synthesis",required=True)
    parser.add_argument("-t", "--timeLimit", help = "time limit for heuristic in seconds",required=True)
    parser.add_argument("-args", "--arguments", help = "arguments of heuristic",required=False, nargs='+')

    filesDict = {}
    # Read arguments from command line
    args = parser.parse_args()
    #choose between -b and -c,-d,-p as input for benchmark informations
    if args.cFiles is not None:
        if (args.dFile is None or args.prjFile is None):
            raise argparse.ArgumentError(None,"error: lacking required arguments")
        filesDict['cFiles'] = args.cFiles
        filesDict['dFile'] = args.dFile
        filesDict['prjFile'] = args.prjFile
    else:
        filesDict['cFiles'] = benchmarks[args.benchmark]["cFiles"]
        filesDict['dFile'] = benchmarks[args.benchmark]["dFile"]
        filesDict['prjFile'] = benchmarks[args.benchmark]["prjFile"]
    filesDict['timeLimit'] = args.timeLimit
    filesDict['model'] = args.estimationModel
    filesDict['heuristic'] = args.heuristic    
    filesDict['saveFile'] = args.saveFile
    filesDict['arguments'] = args.arguments
    
    hour = 3600
    RESOURCE_TO_COMPARE = 'resources'
    modelName = filesDict['model']
    factory = RandomForestFactory(filesDict["dFile"])   
    model = RandomForestEstimator(filesDict['dFile'])
    trainer = RandomSamplesEstimatorTrainer(filesDict,model,5*hour)
    try:
        with open(filesDict['model'], 'rb') as modelFile:
            loadModel = pickle.load(modelFile)
    except Exception as e:
        trainer.trainUntilErrorThreshold(0.8,1.25*hour)
        with open(f'trainers/{modelName}_TRAINER', 'wb') as modelFile:
            pickle.dump(trainer,modelFile)
        with open(f'{modelName}', 'wb') as modelFile:
            pickle.dump(trainer.estimator,modelFile)
    with open(filesDict['model'], 'rb') as modelFile:
        model = pickle.load(modelFile)
    times_dict = {"SHA_MODEL": 5*hour, "GSM_MODEL": 1.25*hour, "AES_MODEL":40*hour,"DIGIT_MODEL":20*hour,"OPTICAL_MODEL":30*hour,"SPAM_MODEL":10*hour,"MOTION_MODEL":5*hour,"ADPCM_MODEL":5*hour}
    GENETIC_HEURISTIC = 'genetic'
    GRASP_HEURISTIC = 'GRASP'
    RANDOM_SEARCH_HEURISTIC = 'random'
    ANT_COLONY_HEURISTIC = 'ACO'

    if (GENETIC_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic1 = GA(filesDict,factory,timeLimit=(int(filesDict['timeLimit'])+10),baseEstimator=model,trainTime=1*hour,solutionSaver=solutionsSaver) 
    elif(GRASP_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic1 = GRASP(filesDict,model,timeLimit=(int(filesDict['timeLimit'])+10),trainTime=1*hour,solutionSaver=solutionsSaver,timeSpentTraining=times_dict[filesDict['model']])   
    elif (RANDOM_SEARCH_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic1 = RandomSearch(filesDict,timeLimit=(int(filesDict['timeLimit'])+10),solutionSaver=solutionsSaver) 
    elif (ANT_COLONY_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic1 = AntColony(filesDict,model,12,0.9,alpha=1,beta=1,timeLimit=(int(filesDict['timeLimit'])+10),trainTime=1*hour,solutionSaver=solutionsSaver) 
        heuristic1.run()
    heuristic1.writeToFile(filesDict['saveFile'])
    
