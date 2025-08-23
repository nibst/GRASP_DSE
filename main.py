import argparse
import copy
import json
import os
import pickle
import time
from directives_impact_analyzer.synthesisBasedDirectivesImpactAnalyzer import  SynthesisBasedDirectivesImpactAnalyzer
from domain.designToolFactory import DesignToolFactory
from domain.mockDesignTool import MockDesignTool
from domain.solution import Solution
from domain.solution_factory import SolutionFactory
from domain.vitisDesignTool import Vitis
from heuristics.impl.grasp.grasp import Grasp
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

def run_heuristic(files_dict, model):
    hour = 3600
    factory = RandomForestFactory(files_dict["dFile"]) 

    GENETIC_HEURISTIC = 'genetic'
    GRASP_HEURISTIC = 'GRASP'
    GRASP_WITH_FREQUENCY_EXPLORATION = "GRASP_FREQUENCY"
    RANDOM_SEARCH_HEURISTIC = 'random'
    ANT_COLONY_HEURISTIC = 'ACO'
    SOFT_PRUNING_GRASP = 'SOFT_PRUNING_GRASP'
    times_dict = {"./models/SHA_MODEL": 5*hour, "./models/GSM_MODEL": 8*hour, "./models/AES_MODEL":40*hour,
                  "./models/DIGIT_MODEL":20*hour,"./models/OPTICAL_MODEL":30*hour,"./models/SPAM_MODEL":10*hour,
                  "./models/MOTION_MODEL":5*hour,"./models/ADPCM_MODEL":5*hour, "./models/new/AES_MODEL":40*hour,
                  "./models/KNN_MODEL": 10*hour, "./models/GEMM_MODEL": 10*hour, "./models/TRANS_FFT_MODEL": 48*hour,
                  "./models/STENCIL3D_MODEL": 5*hour,"./models/BACKPROP_MODEL": 11*hour}
    #choose heuristic
    if (GENETIC_HEURISTIC == files_dict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(files_dict['timeLimit'])/10)
        heuristic = GA(files_dict,factory,timeLimit=(int(files_dict['timeLimit'])+10),baseEstimator=model,trainTime=1*hour,solutionSaver=solutionsSaver) 
    elif(GRASP_HEURISTIC == files_dict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(files_dict['timeLimit'])/10)
        heuristic = Grasp(files_dict,model,time_limit=(int(files_dict['timeLimit'])+10),solution_saver=solutionsSaver,time_spent_training=times_dict[files_dict['model']], explore_target_period=False)   
        heuristic.run()
    elif(GRASP_WITH_FREQUENCY_EXPLORATION == files_dict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(files_dict['timeLimit'])/10)
        #heuristic = GRASP(files_dict,model,timeLimit=(int(files_dict['timeLimit'])+10),trainTime=1*hour,solutionSaver=solutionsSaver,timeSpentTraining=times_dict[files_dict['model']], explore_target_period=True, designTool="mock")   
        if 'start' in files_dict['args'] :
            heuristic = Grasp(files_dict,model,time_limit=(int(files_dict['timeLimit'])+10),solution_saver=solutionsSaver,time_spent_training=times_dict[files_dict['model']], explore_target_period=True, period_exploration_index=0)
        elif 'mid' in files_dict['args']:
            heuristic = Grasp(files_dict,model,time_limit=(int(files_dict['timeLimit'])+10),solution_saver=solutionsSaver,time_spent_training=times_dict[files_dict['model']], explore_target_period=True)
            heuristic.period_exploration_index = int(len(heuristic.exploration_knobs.keys())/2)
        elif 'end' in files_dict['args']:
            heuristic = Grasp(files_dict,model,time_limit=(int(files_dict['timeLimit'])+10),solution_saver=solutionsSaver,time_spent_training=times_dict[files_dict['model']], explore_target_period=True)
            heuristic.period_exploration_index = len(heuristic.exploration_knobs.keys())
        else:
            heuristic = Grasp(files_dict,model,time_limit=(int(files_dict['timeLimit'])+10),solution_saver=solutionsSaver,time_spent_training=times_dict[files_dict['model']], explore_target_period=True)
            heuristic.period_exploration_index = len(heuristic.exploration_knobs.keys()) 
        heuristic.run()

    elif (RANDOM_SEARCH_HEURISTIC == files_dict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(files_dict['timeLimit'])/10)
        heuristic = RandomSearch(files_dict,timeLimit=(int(files_dict['timeLimit'])+10),solutionSaver=solutionsSaver) 
    elif (ANT_COLONY_HEURISTIC == files_dict['heuristic']):
        solutionsSaver = TimeLapsedSolutionsSaver(int(files_dict['timeLimit'])/10)
        heuristic = AntColony(files_dict,model,12,0.9,alpha=1,beta=1,timeLimit=(int(files_dict['timeLimit'])+10),trainTime=1*hour,solutionSaver=solutionsSaver) 
        heuristic.run()
    elif (SOFT_PRUNING_GRASP == files_dict['heuristic']):
        designTool = "vivado"
        directiveImpactAnalyzer = SynthesisBasedDirectivesImpactAnalyzer(designTool)
        with open(files_dict['dFile']) as jsonFile:
            DSEconfig:dict =  json.load(jsonFile)
        directivesDict = DSEconfig['directives']
        dictDir = {}
        for key in directivesDict:
            dictDir[key] = directivesDict[key]['possible_directives']
        directivesImpactFile = f"./directives_impact_analyzer/directives_impact/{designTool}SynthesisBased_{files_dict['benchmark']}.json"
        try:
            with open(directivesImpactFile) as jsonFile:
                directivesImpact:dict =  json.load(jsonFile)
        except Exception as e:
            directiveImpactAnalyzer.getImpacts(dictDir)
            directiveImpactAnalyzer.writeImpactsToFile(directivesImpactFile)
        else:
            directiveImpactAnalyzer.setImpacts(directivesImpact)
        solutionsSaver = TimeLapsedSolutionsSaver(int(files_dict['timeLimit'])/10)
        heuristic = SoftPruningGRASP(files_dict,
                                     model,
                                     timeLimit=(int(files_dict['timeLimit'])+100),
                                     trainTime=1*hour,
                                     solutionSaver=solutionsSaver,
                                     timeSpentTraining=times_dict[files_dict['model']], 
                                     designTool=designTool, 
                                     directivesImpactAnalyzer=directiveImpactAnalyzer)   
        heuristic.run()
    heuristic.writeToFile(files_dict['saveFile'])

def passArgumentsToDictionary(args):
    files_dict = {}
    #choose between -b and -c,-d,-p as input for benchmark informations
    if args.cFiles is not None:
        if (args.dFile is None or args.topFunc is None):
            raise argparse.ArgumentError(None,"error: lacking required arguments")
        files_dict['cFiles'] = args.cFiles
        files_dict['dFile'] = args.dFile
        files_dict['topFunc'] = args.topFunc
    else:
        files_dict['cFiles'] = benchmarks[args.benchmark]["cFiles"]
        files_dict['dFile'] = benchmarks[args.benchmark]["dFile"]
        files_dict['topFunc'] = benchmarks[args.benchmark]["topFunc"]
    files_dict['timeLimit'] = args.timeLimit
    files_dict['model'] = args.estimationModel
    files_dict['heuristic'] = args.heuristic    
    files_dict['saveFile'] = args.saveFile
    files_dict['arguments'] = args.arguments
    files_dict['benchmark'] = args.benchmark
    files_dict['args'] = args.arguments
    return files_dict

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
    parser.add_argument("-p", "--topFunc", help = "Prj. top func",required=False)

    parser.add_argument("-o", "--saveFile", help = "name of save file",required=True)
    parser.add_argument("-model", "--estimationModel", help = "model used in heuristics for estimation of synthesis",required=True)
    parser.add_argument("-t", "--timeLimit", help = "time limit in seconds",required=True)
    parser.add_argument("-args", "--arguments", help = "arguments of heuristic",required=False, nargs='+')
    parser.add_argument("--threshold", help="Error threshold to stop training", type=float, default=0.9)
    parser.add_argument("--trainInterval", help="Training time per threshold check (in seconds)", type=int, default=7200)
    parser.add_argument("--trainOnly", help="Only train estimator, don't run heuristic", action="store_true")
    return parser.parse_args()

def main():

    # Read arguments from command line
    start = time.time()
    args = parseArguments()
    files_dict = passArgumentsToDictionary(args)
    path = f"./dataset/{files_dict['benchmark']}/"
    estimator = RandomForestEstimator(files_dict['dFile'])
    train(path,estimator,files_dict)
    modelName = files_dict['model']
    model = getEstimationModel(modelName)
    #run_heuristic(files_dict,model)
    end = time.time()
    print(f"Total time taken for {files_dict['benchmark']}: {end - start} seconds")

def explore_different_periods(solution:Solution, arguments_dict):
    """
    periods is a list like [3,5,7,10]
    """
    with open( arguments_dict["dFile"]) as json_file:
        dse_config = json.load(json_file)
    periods = [period for period in dse_config["possible_periods"] if period != 8] #exclude 8
    #run synthesis for each period, changing just the period of solution using solution.set_period()
    vitis = Vitis()
    solutions = []
    impl_error_solutions = []
    for period in periods:
        new_solution = copy.deepcopy(solution)

        new_solution.set_period(period)
        # Assuming there is a method to run synthesis
        try:
            new_solution = vitis.runSynthesis(new_solution,arguments_dict['cFiles'],arguments_dict['topFunc'],run_implementation=True)
            solutions.append(new_solution)
        except Exception as e:
            impl_error_solutions.append(new_solution)
    return solutions,impl_error_solutions
def gather_dataset(path, arguments_dict):
    solutions = []
    dse_config_file = arguments_dict['dFile']
    for solution_dir in os.listdir(path):
        solution_path = os.path.join(path, solution_dir)
        if os.path.isdir(solution_path) and os.path.exists(solution_path):
            try:
                solution = SolutionFactory.create_solution_from_vitis_path(solution_path, dse_config_file, filtered=True, is_implementation=True)
                solutions.append(solution)
            except Exception as e:
                error_log_file = "solution_creation_errors.log"
                with open(error_log_file, 'a') as error_file:
                    error_file.write(f"Error creating solution from {solution_path}: {e}\n")

    
    print(f"{arguments_dict["benchmark"]} : {len(solutions)}")
    # random_solutions = random.sample(solutions, min(15, len(solutions)))
    # solutions_with_error = []
    # for solution in random_solutions:
    #     new_solutions,impl_error_solutions = explore_different_periods(solution, arguments_dict)
    #     solutions.extend(new_solutions)
    #     solutions_with_error.extend(impl_error_solutions)
    #     error_solutions_file = f"{arguments_dict['benchmark']}-error-solutions"
    #     if impl_error_solutions:
    #         _extend_solutions_from_file(error_solutions_file,impl_error_solutions)
    #     # Write the updated list back to the file
    #     _extend_solutions_from_file(f"training-{arguments_dict['benchmark']}-solutions",new_solutions)
    return solutions
def _extend_solutions_from_file(file_name,new_solutions):
    try:
        # Try to read existing solutions from the file
        with open(file_name, 'rb') as file:
            existing_solutions = pickle.load(file)
    except (FileNotFoundError, EOFError):
        # If the file does not exist or is empty, initialize an empty list
        existing_solutions = []
    # Extend the existing solutions with the new ones
    existing_solutions.extend(new_solutions)
    # Write the updated list back to the file
    with open(file_name, 'wb') as file:
        pickle.dump(existing_solutions, file)

def train(path,estimator:Estimator, arguments_dict):
    x = gather_dataset(path,arguments_dict)
    estimator.trainModel(x)
    score = estimator.cross_val(x,5)
    #print(f"{arguments_dict['benchmark']}: {str(score)}")
    #with open(f"./models/{arguments_dict['benchmark']}_MODEL3", 'wb') as modelFile:
    #   pickle.dump(estimator,modelFile)

if __name__ == "__main__": 
    with open('./benchmarks/benchmarks.json') as jsonFile:
        benchmarks:dict =  json.load(jsonFile)
    all_benchmarks = ["SHA", "AES", "ADPCM","GSM","GEMM","BACKPROP", "STENCIL3D", "KNN"]
    for benchmark in all_benchmarks:
        with open(f'../last_dse/models/{benchmark}_MODEL','rb') as file:
            a = pickle.load(file)
        x = a.processor.dataset

        print(len(x))
        estimator = RandomForestEstimator(benchmarks[benchmark]["dFile"])
        # args_dict ={}
        # args_dict["dFile"] = benchmarks[benchmark]["dFile"]
        # args_dict["benchmark"] = benchmark
        # train(f"./dataset/{benchmark}/",estimator,args_dict)

        estimator.trainModel(x)
        score = estimator.cross_val(x,5,scorer="cosine_sim").mean()
        print(f"{benchmark} {str(score)}")
    #print(len([solution for solution in a.processor.dataset if solution.period != 8]))
    #main()
