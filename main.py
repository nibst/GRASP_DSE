import argparse
import json
import os
import pickle
from directives_impact_analyzer.synthesisBasedDirectivesImpactAnalyzer import  SynthesisBasedDirectivesImpactAnalyzer
from domain.designToolFactory import DesignToolFactory
from domain.solution import Solution
from domain.solution_factory import SolutionFactory
from domain.vitisDesignTool import Vitis
from predictor.estimators.estimator import Estimator
from heuristics.heuristic import Heuristic
from heuristics.impl.antColony import AntColony
from heuristics.impl.exhaustiveSearch import ExhaustiveSearch
from heuristics.impl.genetic import GA
from heuristics.impl.GRASP import GRASP
from heuristics.impl.greedy import Greedy
from heuristics.impl.hillClimbing0 import HillClimbing
from heuristics.impl.RandomSearch import RandomSearch
from heuristics.impl.randomSearchWithEstimator import RandomSearchWithEstimator
from heuristics.impl.softPruningGRASP import SoftPruningGRASP
from predictor.estimators.randomforest.randomForest import \
    RandomForestEstimator
from predictor.estimators.randomforest.randomForestFactory import \
    RandomForestFactory
from utils.estimatorTrainer import RandomSamplesEstimatorTrainer
from utils.timeLapsedSolutionsSaver import TimeLapsedSolutionsSaver
import random

def run_heuristic(filesDict, model):
    hour = 3600
    factory = RandomForestFactory(filesDict["dFile"]) 

    GENETIC_HEURISTIC = 'genetic'
    GRASP_HEURISTIC = 'GRASP'
    RANDOM_SEARCH_HEURISTIC = 'random'
    ANT_COLONY_HEURISTIC = 'ACO'
    SOFT_PRUNING_GRASP = 'SOFT_PRUNING_GRASP'
    times_dict = {"./models/SHA_MODEL": 5*hour, "./models/GSM_MODEL": 1.25*hour, "./models/AES_MODEL":40*hour,
                  "./models/DIGIT_MODEL":20*hour,"./models/OPTICAL_MODEL":30*hour,"./models/SPAM_MODEL":10*hour,
                  "./models/MOTION_MODEL":5*hour,"./models/ADPCM_MODEL":5*hour, "./models/new/AES_MODEL":40*hour,
                  "./models/test/ADPCM_MODEL": 5*hour}
    #choose heuristic
    if (GENETIC_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic = GA(filesDict,factory,timeLimit=(int(filesDict['timeLimit'])+10),baseEstimator=model,trainTime=1*hour,solutionSaver=solutionsSaver) 
    elif(GRASP_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic = GRASP(filesDict,model,timeLimit=(int(filesDict['timeLimit'])+10),trainTime=1*hour,solutionSaver=solutionsSaver,timeSpentTraining=times_dict[filesDict['model']])   
        heuristic.run()
    elif (RANDOM_SEARCH_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic = RandomSearch(filesDict,timeLimit=(int(filesDict['timeLimit'])+10),solutionSaver=solutionsSaver) 
    elif (ANT_COLONY_HEURISTIC == filesDict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic = AntColony(filesDict,model,12,0.9,alpha=1,beta=1,timeLimit=(int(filesDict['timeLimit'])+10),trainTime=1*hour,solutionSaver=solutionsSaver) 
        heuristic.run()
    elif (SOFT_PRUNING_GRASP == filesDict['heuristic']):
        designTool = "vivado"
        directiveImpactAnalyzer = SynthesisBasedDirectivesImpactAnalyzer(designTool)
        with open(filesDict['dFile']) as jsonFile:
            DSEconfig:dict =  json.load(jsonFile)
        directivesDict = DSEconfig['directives']
        dictDir = {}
        for key in directivesDict:
            dictDir[key] = directivesDict[key]['possible_directives']
        directivesImpactFile = f"./directives_impact_analyzer/directives_impact/{designTool}SynthesisBased_{filesDict['benchmark']}.json"
        try:
            with open(directivesImpactFile) as jsonFile:
                directivesImpact:dict =  json.load(jsonFile)
        except Exception as e:
            directiveImpactAnalyzer.getImpacts(dictDir)
            directiveImpactAnalyzer.writeImpactsToFile(directivesImpactFile)
        else:
            directiveImpactAnalyzer.setImpacts(directivesImpact)
        solutionsSaver = TimeLapsedSolutionsSaver(int(filesDict['timeLimit'])/10)
        heuristic = SoftPruningGRASP(filesDict,
                                     model,
                                     timeLimit=(int(filesDict['timeLimit'])+100),
                                     trainTime=1*hour,
                                     solutionSaver=solutionsSaver,
                                     timeSpentTraining=times_dict[filesDict['model']], 
                                     designTool=designTool, 
                                     directivesImpactAnalyzer=directiveImpactAnalyzer)   
        heuristic.run()
    heuristic.writeToFile(filesDict['saveFile'])

def passArgumentsToDictionary(args):
    filesDict = {}
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
    filesDict['benchmark'] = args.benchmark
    return filesDict

def getEstimationModel(modelName):
    #try to open model file for estimation
    try:
        with open(modelName, 'rb') as modelFile:
            model = pickle.load(modelFile)
    except Exception as e:
        raise

    return model

def parseArguments():
    parser = argparse.ArgumentParser()
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
    return parser.parse_args()

def main():
    # with open('./dse/GRASP_ADPCM2h_preTrained', 'rb') as dse_file:
    #     dse_data = pickle.load(dse_file)
    
    # solutions = dse_data.solutions
    # indices = [
    #     [1, 2],
    #     [3, 4],
    #     [5, 6],
    #     [7, 8],
    #     [9],
    #     [10],
    #     [11, 12],
    #     [13],
    #     [14],
    #     [15]
    # ]
    
    # for i, index_list in enumerate(indices):
    #     with open(f'timeStampFiller{i}', 'wb') as file:
    #         solutions_to_save = []
    #         for index in index_list:
    #             solutions_to_save.append(solutions[index-1])
    #         pickle.dump(solutions_to_save, file)

    # Read arguments from command line
    args = parseArguments()
    filesDict = passArgumentsToDictionary(args)
    path = f"./dataset/{filesDict['benchmark']}/"
    estimator = RandomForestEstimator(filesDict['dFile'])
    train(path,estimator,filesDict)
    modelName = filesDict['model']
    model = getEstimationModel(modelName)
    #run_heuristic(filesDict,model)

def explore_different_periods(solution:Solution, arguments_dict):
    """
    periods is a list like [3,5,7,10]
    """
    with open( arguments_dict["dFile"]) as json_file:
        dse_config = json.load(json_file)
    periods = dse_config["possible_periods"]
    #run synthesis for each period, changing just the period of solution using solution.set_period()
    vitis = Vitis()
    solutions = []
    for period in periods:
        solution.set_period(period)
        # Assuming there is a method to run synthesis
        solution = vitis.runSynthesis(solution,arguments_dict['cFiles'],arguments_dict['prjFile'],run_implementation=True)
        solutions.append(solution)
        with open(f"{arguments_dict['benchmark']}-solutions", 'wb') as file:
            pickle.dump(solutions, file)
    return solutions
def gather_dataset(path, arguments_dict):
    solutions = []
    dse_config_file = arguments_dict['dFile']
    for solution_dir in os.listdir(path):
        solution_path = os.path.join(path, solution_dir)
        if os.path.isdir(solution_path) and os.path.exists(solution_path):
            solution = SolutionFactory.create_solution_from_vitis_path(solution_path, dse_config_file)
            solutions.append(solution)
    
    # Select a random sample of 15 solutions
    random_solutions = random.sample(solutions, min(15, len(solutions)))
    for solution in random_solutions:
        new_solutions = explore_different_periods(solution, arguments_dict)
        solutions.extend(new_solutions)
    return solutions
    
def train(path,estimator:Estimator, arguments_dict):
    x = gather_dataset(path,arguments_dict)
    estimator.trainModel(x)
    score = estimator.cross_val(x,5)
    print(f"{arguments_dict['benchmark']}: {str(score)}")
    with open(f'./models/{arguments_dict['benchmark']}_MODEL', 'wb') as modelFile:
        pickle.dump(estimator,modelFile)

if __name__ == "__main__": 
    with open('./benchmarks/benchmarks.json') as jsonFile:
        benchmarks:dict =  json.load(jsonFile)
    # with open('GSM-solutions', 'rb') as file:
    #    solutions = pickle.load(file)
    # print(solutions)
    main()




