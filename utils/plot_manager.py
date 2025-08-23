import os
import pickle
from typing import List
from heuristics.heuristic import Heuristic
from utils.heuristic_solutions import HeuristicSolutions
from utils.ADRS import ADRS
from utils.graphs import Graphs
from utils.paretoComparer import ParetoComparer
from utils.plotMaker import PlotMaker
import matplotlib.pyplot as plt

from utils.statistics import arithmetic_mean_adrs, arithmetic_mean_percentage, geometric_mean

class PlotManager:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        
    def all_heuristics_in_one_bar(self, method: str, solutions_of_all_heuristics: List[HeuristicSolutions], benchmarks: List[str], number_of_timestamps: int, metrics = ['resources', 'time_latency']):
        """
        Generate a bar plot comparing all heuristics for a given method (e.g., ADRS or PERCENTAGE).
        """
        method = method.upper()
        myplt = PlotMaker(method, 'Heuristics', "Average")
        averages = {}
        means = {}
        heuristic_names_map = {"GRASP": "GRASP baseline", "GRASP_FREQUENCY_start": "GRASP start", 
                               "GRASP_FREQUENCY_mid": "GRASP mid", "GRASP_FREQUENCY_end": "GRASP end"}

        for benchmark in benchmarks:
            if method == "PERCENTAGE":
                all_solutions = self.get_all_solutions_from_benchmark(solutions_of_all_heuristics, benchmark, number_of_timestamps,include_model=True)

                for heuristic in solutions_of_all_heuristics:
                    name = heuristic.heuristic_name
                    if name not in averages:
                        averages[name] = []
                    if name not in means:
                        means[name] = 0
                    averages[name].append(arithmetic_mean_percentage([heuristic.solutions_timestamps_per_benchmark[benchmark][-1]], [all_solutions[-1]],metrics=metrics))
                    means[name] = sum(averages[name]) / len(averages[name])

            elif method == "ADRS":
                all_solutions = self.get_all_solutions_from_benchmark(solutions_of_all_heuristics, benchmark, number_of_timestamps, include_model=True)

                for heuristic in solutions_of_all_heuristics:
                    heuristic_name = heuristic.heuristic_name
                    if heuristic_name not in averages:
                        averages[heuristic_name] = []
                    if heuristic_name not in means:
                        means[heuristic_name] = 0

                    averages[heuristic_name].append(arithmetic_mean_adrs(all_solutions[-1], [heuristic.solutions_timestamps_per_benchmark[benchmark][-1]], metrics=metrics))
                    means[heuristic_name] = geometric_mean(averages[heuristic_name])

        max_value = max(means.values())
        plt.ylim(0, max_value + max_value / 6)
        heuristics = [heuristic_names_map[heuristic.heuristic_name] for heuristic in solutions_of_all_heuristics]
        print(f"Means: {means}")
        myplt.barPlot(heuristics, [mean for mean in means.values()], width=0.6)
        plt.savefig(os.path.join(self.output_dir, f"{method}_summarizedBarPlot.png"))

        myplt.showPlot()
        
    def plot_heuristics_comparison(self, method: str, solutions_of_all_heuristics: List[HeuristicSolutions], benchmarks: List[str], save_interval: int, metrics=['resources', 'time_latency']):
        method = method.upper()
        for benchmark in benchmarks:
            if method == "PERCENTAGE":
                all_solutions_per_timestamp = self.get_all_solutions_from_benchmark(solutions_of_all_heuristics, benchmark, include_model=True)
                self._plot_percentage(benchmark, solutions_of_all_heuristics, all_solutions_per_timestamp, save_interval, metrics=metrics)
            elif method == "ADRS":
                all_solutions_per_timestamp = self.get_all_solutions_from_benchmark(solutions_of_all_heuristics, benchmark,include_model=True)
                self._plot_adrs(benchmark, solutions_of_all_heuristics, all_solutions_per_timestamp[-1], save_interval, metrics=metrics)

    def _plot_percentage(self, benchmark, solutions_of_all_heuristics, all_solutions, save_interval, metrics=['resources', 'time_latency']):
        myplt = PlotMaker(benchmark, 'minutes', "Pareto Dominance")
        myplt.ylim(0, 1.1)
        comparer = ParetoComparer(metrics[0], metrics[1])
        for heuristic in solutions_of_all_heuristics:
            Graphs.plotParetoPercentage(
                myplt, comparer, heuristic.solutions_timestamps_per_benchmark[benchmark], all_solutions,
                heuristic.heuristic_name, save_interval
            )
        lns = myplt.lns[0]
        for i in range(len(myplt.lns) -1):
            lns += myplt.lns[i+1]
        
        labs = [l.get_label() for l in lns]
        myplt.ax.legend(lns, labs, loc=0)
        plt.savefig(os.path.join(self.output_dir, f"PERCENTAGE_allHeuristics_{benchmark}.png"))

        myplt.showPlot()


    def _plot_adrs(self, benchmark, solutions_of_all_heuristics, all_solutions, save_interval, metrics=['resources', 'time_latency']):
        myplt = PlotMaker(benchmark, 'minutes', "ADRS")
        comparer = ADRS(metrics[0], metrics[1])
        for heuristic in solutions_of_all_heuristics:
            print(f"bench {benchmark} heuristic {heuristic.heuristic_name}")
            Graphs.plotADRS(
                myplt, comparer, all_solutions, heuristic.solutions_timestamps_per_benchmark[benchmark],
                heuristic.heuristic_name, save_interval
            )
        lns = myplt.lns[0]
        for i in range(len(myplt.lns) -1):
            lns += myplt.lns[i+1]
        
        labs = [l.get_label() for l in lns]
        myplt.ax.legend(lns, labs, loc=0)
        plt.savefig(os.path.join(self.output_dir, f"ADRS_allHeuristics_{benchmark}.png"))

        myplt.showPlot()


    def get_all_solutions_from_benchmark(self, solutions_of_all_heuristics, benchmark, number_of_timestamps=10, include_model=False):
        with open(f"./models/{benchmark}_MODEL", "rb") as f:
            model = pickle.load(f)
        all_solutions = []
        for i in range(number_of_timestamps):
            time_stamp_all_solutions = []
            for heuristic in solutions_of_all_heuristics:
                time_stamp_all_solutions.extend(heuristic.solutions_timestamps_per_benchmark[benchmark][i])
            if include_model:
                time_stamp_all_solutions.extend(model.processor.dataset)
            all_solutions.append(time_stamp_all_solutions)

        return all_solutions
    
# def check_paretos_with_different_period(solutions_of_all_heuristics, benchmark, number_of_timestamps):
    # for heuristic in solutions_of_all_heuristics:
    #     if heuristic.heuristic_name == 'GRASP_FREQUENCY':
    #         all_solutions = [heuristic.solutions_timestamps_per_benchmark[benchmark][i] for i in range(number_of_timestamps)]
    # paretos = Heuristic.paretoSolutions('resources', 'time_latency', solutions=all_solutions[9])
    # paretos_with_different_period = [pareto for pareto in paretos if pareto.period != 8]
    # count_different_period = len(paretos_with_different_period)
    # total_paretos = len(paretos)
    # print(f"Number of paretos with period != 8: {count_different_period} out of {total_paretos}")