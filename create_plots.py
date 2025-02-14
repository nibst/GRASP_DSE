import copy
import os
from typing import List
from domain.solution import Solution
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
import matplotlib.pyplot as plt
from utils.plotMaker import PlotMaker
from utils.ADRS import ADRS
import pickle
import numpy as np
from heuristics.heuristic import Heuristic

# benchmarks = ["SHA","GSM","AES","SPAM","MOTION","ADPCM","DIGIT"]
benchmarks = ["SHA","GSM","AES","ADPCM"]

class HeuristicSolutions:
    def __init__(self, heuristic_name: str, solutions_timestamps_per_benchmark: dict[list[List[Solution]]]):
        self.heuristic_name = heuristic_name
        self.solutions_timestamps_per_benchmark = solutions_timestamps_per_benchmark

def main():
    grasp_timestamps_per_benchmark = {}
    genetic_timestamps_per_benchmark = {} 
    aco_timestamps_per_benchmark = {}
    for benchmark in benchmarks:
        genetic = Graphs.pathToListsOfSolutions(f"./saves/saves_with_model/genetic_{benchmark}_2h/")
        grasp  = Graphs.pathToListsOfSolutions(f"./saves/saves_with_model/GRASP_{benchmark}_2h/")
        aco = Graphs.pathToListsOfSolutions(f"./saves/saves_with_model/ACO_{benchmark}_2h/")
        # soft_grasp = Graphs.pathToListsOfSolutions(f"../saves_patati/savesWithModel/SOFT_PRUNING_GRASP_{benchmark}_2h/")
        grasp_timestamps_per_benchmark[benchmark] = grasp
        genetic_timestamps_per_benchmark[benchmark] = genetic
        aco_timestamps_per_benchmark[benchmark] = aco
    solutions_of_all_heuristics = []    
    solutions_of_all_heuristics.append(HeuristicSolutions("ACO", aco_timestamps_per_benchmark)) 
    solutions_of_all_heuristics.append(HeuristicSolutions("GRASP", grasp_timestamps_per_benchmark))
    solutions_of_all_heuristics.append(HeuristicSolutions("GENETIC", genetic_timestamps_per_benchmark))
                                    
    all_heuristics_in_one_bar("PERCENTAGE", solutions_of_all_heuristics, 10)
    all_heuristics_in_one_bar("ADRS", solutions_of_all_heuristics, 10)

    plot_heuristics_comparison("PERCENTAGE", solutions_of_all_heuristics, 12*60, 10)
    plot_heuristics_comparison("ADRS", solutions_of_all_heuristics, 12*60, 10)

def plot_heuristics_comparison(method: str, solutions_of_all_heuristics: List[HeuristicSolutions], save_interval, number_of_timestamps):
    method = method.upper()
    benchmarks = ["SHA","GSM","AES","ADPCM"]
    DEFAULT_LINEWIDTH = 4
    DEFAULT_LINEWIDTH_DECAY = 0.8
    for benchmark in benchmarks:
        all_solutions = copy.deepcopy(solutions_of_all_heuristics[0].solutions_timestamps_per_benchmark[benchmark][number_of_timestamps-1])
        for i in range(1, len(solutions_of_all_heuristics)):
            all_solutions.extend(solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark][number_of_timestamps-1])
        
        if method == "PERCENTAGE":
            myplt = PlotMaker(benchmark, 'minutes', "Pareto Dominance")
            myplt.ylim(0, 1.1)
            all_solutions = [all_solutions] * number_of_timestamps # solutions_of_all_heuristics[0].number_of_timestamps

            comparer = ParetoComparer('resources', 'latency')
            linewidth = DEFAULT_LINEWIDTH
            for i in range(len(solutions_of_all_heuristics)):
                Graphs.plotParetoPercentage(myplt, comparer, solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark], all_solutions,
                                            solutions_of_all_heuristics[i].heuristic_name, save_interval, linewidth=linewidth)
                linewidth = linewidth * DEFAULT_LINEWIDTH_DECAY

            lns = myplt.lns[0]
            for i in range(len(myplt.lns) -1):
                lns += myplt.lns[i+1]
            
            labs = [l.get_label() for l in lns]
            myplt.ax.legend(lns, labs, loc=0)
            
        if method == "ADRS":
            myplt = PlotMaker(benchmark, 'minutes', "ADRS")

            comparer = ADRS('resources', 'latency')
            worst_adrs = float("-inf")
            for i in range(len(solutions_of_all_heuristics)):
                adrs = comparer.compare(all_solutions, solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark][0])
                if adrs is None:
                    adrs = 0
                if adrs > worst_adrs:
                    worst_adrs = adrs
            plt.ylim(0, worst_adrs + worst_adrs / 7)

            linewidth = DEFAULT_LINEWIDTH
            for i in range(len(solutions_of_all_heuristics)):
                Graphs.plotADRS(myplt, comparer, all_solutions, solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark],
                                solutions_of_all_heuristics[i].heuristic_name, save_interval, linewidth=linewidth)
                linewidth = DEFAULT_LINEWIDTH_DECAY

            lns = myplt.lns[0]
            for i in range(len(myplt.lns) -1):
                lns += myplt.lns[i+1]
                
            labs = [l.get_label() for l in lns]
            myplt.ax.legend(lns, labs, loc=0)

        # plt.savefig(f'../schwarzenegger/plotsPNG/{method}/{method}_allHeuristics_{benchmark}.png')
        myplt.showPlot()

def all_heuristics_in_one_bar(method: str, solutions_of_all_heuristics: List[HeuristicSolutions], number_of_timestamps):
    method = method.upper()
    benchmarks = ["SHA","GSM","AES","ADPCM"]
    myplt = PlotMaker(method, 'Heuristics', "Average")
    averages = {}
    means = {}
    # initialize
    for i in range(len(solutions_of_all_heuristics)):
        averages[solutions_of_all_heuristics[i].heuristic_name] = []
        means[solutions_of_all_heuristics[i].heuristic_name] = []
    heuristics = list(heuristic.heuristic_name for heuristic in solutions_of_all_heuristics)

    for benchmark in benchmarks:
        all_solutions = copy.deepcopy(solutions_of_all_heuristics[0].solutions_timestamps_per_benchmark[benchmark][number_of_timestamps-1])
        for i in range(1, len(solutions_of_all_heuristics)):
            all_solutions.extend(solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark][number_of_timestamps-1])
        
        if method == "PERCENTAGE":
            all_solutions = [all_solutions] * 10
            for i in range(len(solutions_of_all_heuristics)):
                name = solutions_of_all_heuristics[i].heuristic_name
                averages[name].append(arithmetic_mean_percentage(solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark], all_solutions))
                means[name] = sum(averages[name]) / len(averages[name])

        if method == "ADRS":
            # average ADRS: avg of all best ADRS through time from one heuristic
            for i in range(len(solutions_of_all_heuristics)):
                heuristic_name = solutions_of_all_heuristics[i].heuristic_name
                averages[heuristic_name].append(arithmetic_mean_adrs(all_solutions, solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark]))
                means[heuristic_name] = geometric_mean(averages[heuristic_name])
            
    # max_value = max(mean_soft_grasp, mean_grasp)
    # plt.ylim(0, max_value + max_value / 6)
    # myplt.barPlot(heuristics, [mean_soft_grasp, mean_grasp], width=0.6)
    max_value = max([mean for mean in means.values()])
    plt.ylim(0, max_value + max_value / 6)
    myplt.barPlot(heuristics, [mean for mean in means.values()], width=0.6)
    # plt.savefig(f'../schwarzenegger/plotsPNG/{method}/{method}_summarizedBarPlot.png')

    myplt.showPlot()

def geometric_mean(iterable: list):
    a = np.array(iterable)
    length = len(a)
    for i in range(length):
        if a[i] == 0:
            a = np.delete(a, i)
    return a.prod() ** (1.0 / len(a))

def arithmetic_mean_adrs(reference_set, solutions):
    comparer = ADRS('resources', 'latency')
    all_best_adrs = []
    for i in range(len(solutions)):
        all_best_adrs.append(comparer.compare(reference_set, solutions[i]))
    filtered_items = filter(lambda item: item is not None, all_best_adrs)
    new_lst = list(filtered_items)
    return np.mean(new_lst)

def arithmetic_mean_percentage(solutions1, solutions2):
    comparer = ParetoComparer('resources', 'latency')
    all_best_percentage = []
    for i in range(len(solutions1)):
        all_best_percentage.append(comparer.compare(solutions1[i], solutions2[i]))
    filtered_items = filter(lambda item: item is not None, all_best_percentage)
    new_lst = list(filtered_items)
    return np.mean(new_lst)

main()

# use for adding estimators solutions to heuristics solution
"""
    for benchmark in benchmarks:
        model_file = f"./models/{benchmark}_MODEL"
        with open(model_file, "rb") as f:
            model: RandomForestEstimator = pickle.load(f)
        a = model.processor.dataset
        grasp_dir = f"./saves/GRASP_{benchmark}_2h/"
        for filename in os.listdir(grasp_dir):
            with open(os.path.join(grasp_dir, filename), "rb") as heuristicfile:
                b = pickle.load(heuristicfile)
            with open(os.path.join(f"./saves/saves_with_model/GRASP_{benchmark}_2h/", filename), "wb") as heuristicfile:
                b.extend(a)
                pickle.dump(b, heuristicfile)
"""