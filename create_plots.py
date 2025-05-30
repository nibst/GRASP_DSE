import copy
import os
from typing import List
from domain.solution import Solution
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
from utils.benchmark_manager import BenchmarkManager
from utils.graphs import Graphs 
from utils.heuristic_solutions import HeuristicSolutions
from utils.paretoComparer import ParetoComparer
import matplotlib.pyplot as plt
from utils.plotMaker import PlotMaker
from utils.ADRS import ADRS
import pickle
import numpy as np
from heuristics.heuristic import Heuristic
from utils.plot_manager import PlotManager

benchmarks = ["SHA", "AES", "ADPCM","GSM","TRANS_FFT","GEMM","KNN"]


def main():


    base_path = "."
    output_dir = "./plots_png"

    # Initialize managers
    benchmark_manager = BenchmarkManager(base_path)
    plot_manager = PlotManager(output_dir)

    # Load heuristic solutions
    solutions_of_all_heuristics = []
    for heuristic_name in ["GRASP_FREQUENCY_end", "GRASP_FREQUENCY_start","GRASP_FREQUENCY_mid"]:
        timestamps_per_benchmark = {
            benchmark: benchmark_manager.load_solutions_timestamps(heuristic_name, benchmark)
            for benchmark in benchmarks
        }
        solutions_of_all_heuristics.append(HeuristicSolutions(heuristic_name, timestamps_per_benchmark))

    for heuristic_solutions in solutions_of_all_heuristics:
        for benchmark in heuristic_solutions.solutions_timestamps_per_benchmark:
            # save the solutions of each heuristic to a file
            heuristic_name = heuristic_solutions.heuristic_name
            benchmark_timestamps = heuristic_solutions.solutions_timestamps_per_benchmark[benchmark]
            filtered_solutions = [sol for sol in benchmark_timestamps[-1] if sol.period != 8]
            with open(f"{heuristic_name}_data.txt", "a") as output_file:
                all_solutions_per_timestamp = plot_manager.get_all_solutions_from_benchmark(solutions_of_all_heuristics, benchmark,include_model=False)
                percentage = len(filtered_solutions)/len(benchmark_timestamps[-1]) * 100
                pareto_comparer = ParetoComparer("resources", "latency")
                pareto_comparsion = pareto_comparer.compare(filtered_solutions, all_solutions_per_timestamp[-1])
                paretos = f"Percentage of paretos that have period != 8: {pareto_comparsion*100}%"
                proportion = f"{benchmark} {len(filtered_solutions)}/{len(benchmark_timestamps[-1])} {percentage}%\n{paretos}\n"

                output_file.write(proportion)
    # Generate plots
    # plot_manager.all_heuristics_in_one_bar("ADRS", solutions_of_all_heuristics, benchmarks,10)
    # plot_manager.all_heuristics_in_one_bar("PERCENTAGE", solutions_of_all_heuristics, benchmarks,10)
    # plot_manager.plot_heuristics_comparison("PERCENTAGE", solutions_of_all_heuristics, benchmarks, 24 * 60, 10)
    # plot_manager.plot_heuristics_comparison("ADRS", solutions_of_all_heuristics, benchmarks, 24 * 60, 10)





def all_heuristics_in_one_bar(method: str, solutions_of_all_heuristics: List[HeuristicSolutions], number_of_timestamps):
    method = method.upper()
    myplt = PlotMaker(method, 'Heuristics', "Average")
    averages = {}
    means = {}
    # initialize

    heuristics = list(heuristic.heuristic_name for heuristic in solutions_of_all_heuristics)

    for benchmark in benchmarks:
        # all_solutions = copy.deepcopy(solutions_of_all_heuristics[0].solutions_timestamps_per_benchmark[benchmark][number_of_timestamps-1])
        # for i in range(1, len(solutions_of_all_heuristics)):
        #     all_solutions.extend(solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark][number_of_timestamps-1])
        all_solutions = get_all_solutions_from_benchmark(solutions_of_all_heuristics,benchmark)
        if method == "PERCENTAGE":
            all_solutions = [all_solutions] * 10
            for i in range(len(solutions_of_all_heuristics)):
                name = solutions_of_all_heuristics[i].heuristic_name
                if name not in averages:
                    averages[name] = []
                if name not in means:
                    means[name] = 0
                averages[name].append(arithmetic_mean_percentage(solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark], all_solutions))
                means[name] = sum(averages[name]) / len(averages[name])

        if method == "ADRS":
            # average ADRS: avg of all best ADRS through time from one heuristic
            for i in range(len(solutions_of_all_heuristics)):
                heuristic_name = solutions_of_all_heuristics[i].heuristic_name
                if heuristic_name not in averages:
                    averages[heuristic_name] = []
                if heuristic_name not in means:
                    means[heuristic_name] = 0

                averages[heuristic_name].append(arithmetic_mean_adrs(all_solutions, solutions_of_all_heuristics[i].solutions_timestamps_per_benchmark[benchmark]))
                means[heuristic_name] = geometric_mean(averages[heuristic_name])
            
    # max_value = max(mean_soft_grasp, mean_grasp)
    # plt.ylim(0, max_value + max_value / 6)
    # myplt.barPlot(heuristics, [mean_soft_grasp, mean_grasp], width=0.6)
    max_value = max([mean for mean in means.values()])
    plt.ylim(0, max_value + max_value / 6)
    myplt.barPlot(heuristics, [mean for mean in means.values()], width=0.6)
    plt.savefig(f'./plots_png/{method}/{method}_summarizedBarPlot.png')

    myplt.showPlot()

def geometric_mean(iterable: list):
    a = np.array(iterable)
    length = len(a)
    for i in range(length):
        #add a little e value to all elements of array
        e = 0.1
        if a[i]:
            a[i] += e
    # remove None values
    filtered_array = a[a != None]
    return filtered_array.prod() ** (1.0 / len(filtered_array))

def arithmetic_mean_adrs(reference_set, timestamps):
    comparer = ADRS('resources', 'latency')
    all_best_adrs = []
    for i in range(len(timestamps)):
        all_best_adrs.append(comparer.compare(reference_set, timestamps[i]))
    filtered_items = filter(lambda item: item is not None, all_best_adrs)
    new_lst = list(filtered_items)
    if new_lst == []:
        return None
    return np.mean(new_lst)

def arithmetic_mean_percentage(solutions1, solutions2):
    comparer = ParetoComparer('resources', 'latency')
    all_best_percentage = []
    for i in range(len(solutions1)):
        all_best_percentage.append(comparer.compare(solutions1[i], solutions2[i]))
    filtered_items = filter(lambda item: item is not None, all_best_percentage)
    new_lst = list(filtered_items)
    return np.mean(new_lst)

def get_all_solutions_from_benchmark(solutions_of_all_heuristics,benchmark):
    all_solutions = []
    with open(f"./models/{benchmark}_MODEL", "rb") as f:
        model = pickle.load(f)
    for heuristic in solutions_of_all_heuristics:
        all_solutions.extend(heuristic.solutions_timestamps_per_benchmark[benchmark][9])
    #all_solutions.extend(model.processor.dataset)

    return all_solutions
main()
