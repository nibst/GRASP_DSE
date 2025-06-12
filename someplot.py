import matplotlib.pyplot as plt
from heuristics.heuristic import Heuristic
from utils.benchmark_manager import BenchmarkManager
from utils.heuristic_solutions import HeuristicSolutions
from utils.plotMaker import PlotMaker
from utils.graphs import Graphs
from utils.plot_manager import PlotManager
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
from scipy.interpolate import make_interp_spline

def plot_pareto_frontiers_with_highlight(plot_manager, solutions_of_all_heuristics, benchmark, output_dir):
    """
    Generate two Pareto frontier plots:
    1. One for GRASP (default frequency).
    2. One for GRASP_FREQUENCY_mid (different frequencies).
    Combine the two and highlight Pareto solutions with different frequencies.
    """
    metrics = ['resources', 'time_latency']
    colors = ['blue', 'seagreen']
    # Initialize PlotMaker
    plot_maker = PlotMaker(benchmark, metrics[0], metrics[1])

    # Load solutions for GRASP and GRASP_FREQUENCY_mid
    all_solutions = plot_manager.get_all_solutions_from_benchmark(solutions_of_all_heuristics, benchmark, include_model=False)

    # Extract solutions from the last timestamp
    all_solutions_from_last_timestamp = all_solutions[-1]  # Get the last timestamp solutions
    # Filter solutions to only include those with period == 8
    all_solutions_without_frequency = [sol for sol in all_solutions_from_last_timestamp if sol.period == 8]

    """
    The opaque solutions must be the globally pareto frontier.
    Transparents solutions are the solutions that were pareto optimal in one of the groups but not in the pareto frontier of the whole set.
    """
    paretos_of_solutions_without_frequency = Heuristic.paretoSolutions(metrics[0], metrics[1], solutions=all_solutions_without_frequency)
    top_ylim = max([solution.results[metrics[1]] for solution in paretos_of_solutions_without_frequency])

    top_ylim = 0
    for heuristic in solutions_of_all_heuristics:
        marker = 'o'  # Default marker
        if heuristic.get_name() == "GRASP_FREQUENCY_start":
            marker = '^'
        elif heuristic.get_name() == "GRASP_FREQUENCY_mid":
            marker = '*'
        elif heuristic.get_name() == "GRASP_FREQUENCY_end":
            marker = '+'
        else:
            continue
        solutions_with_frequency = [sol for sol in heuristic.get_timestamps(benchmark)[-1] if sol.period != 8]
        paretos = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=all_solutions_from_last_timestamp)
        Graphs.plot_solutions_intersections(plot_maker, solutions=paretos, my_solutions=solutions_with_frequency, metrics=metrics, color=colors[1], marker=marker)   
        Graphs.plot_paretos(plot_maker, solutions=solutions_with_frequency, secondary_marker=marker, secondary_color=colors[1], main_opacity=0.0,secondary_opacity=0.3,only_non_default_freq=True)

        top_ylim = max(top_ylim,max([solution.results[metrics[1]] for solution in paretos]))

    # Create custom legend handles
    non_default_freq_patch = mpatches.Patch(color=colors[1], label='Non-default frequency')
    default_freq_patch = mpatches.Patch(color=colors[0], label='Default frequency')     
    Graphs.plot_paretos(plot_maker, solutions=all_solutions_from_last_timestamp,main_opacity=1,secondary_opacity=0.0, only_default_freq=True)
    Graphs.plot_paretos(plot_maker, solutions=all_solutions_without_frequency,main_opacity=0.3,secondary_opacity=0.0)
    plt.savefig(f"{output_dir}/frequency/pareto_with_frequency{benchmark}.png")

    marker_triangle = mlines.Line2D([], [], color=colors[1], marker='^', markersize=10, linestyle='None', label='Frequency explored at start of GRC')
    marker_star     = mlines.Line2D([], [], color=colors[1], marker='*', markersize=10, linestyle='None', label='Frequency explored at middle of GRC')
    marker_plus     = mlines.Line2D([], [], color=colors[1], marker='+', markersize=10, linestyle='None', label='Frequency explored at end of GRC')
    # Generate smooth curve
    paretos = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=all_solutions_from_last_timestamp)
    x = np.array([solution.results[metrics[0]] for solution in paretos])
    y = np.array([solution.results[metrics[1]] for solution in paretos])
    x_sorted, y_sorted = zip(*sorted(zip(x, y)))

    # Plot pareto frontier line
    plt.plot(x_sorted, y_sorted, color='darkred', alpha=0.5)
    # Add combined legend
    plt.legend(handles=[non_default_freq_patch, default_freq_patch, marker_triangle, marker_star, marker_plus], loc='best',prop={'size': 10})

    plot_maker.showPlot()

# Example usage
def main():
    base_path = "."
    output_dir = "./plots_png"
    benchmarks = ["SHA", "AES", "ADPCM","GSM","TRANS_FFT","GEMM","KNN","BACKPROP","STENCIL3D"]

    # Initialize PlotManager
    benchmark_manager = BenchmarkManager(base_path)
    plot_manager = PlotManager(output_dir)
    
    # Load heuristic solutions
    solutions_of_all_heuristics = []
    for heuristic_name in ["GRASP","GRASP_FREQUENCY_start","GRASP_FREQUENCY_mid","GRASP_FREQUENCY_end"]:
        timestamps_per_benchmark = {
            benchmark: benchmark_manager.load_solutions_timestamps(heuristic_name, benchmark)
            for benchmark in benchmarks
        }
        solutions_of_all_heuristics.append(HeuristicSolutions(heuristic_name, timestamps_per_benchmark))


    # Generate the plots
    for benchmark in benchmarks:
        plot_pareto_frontiers_with_highlight(plot_manager, solutions_of_all_heuristics, benchmark, output_dir)

main()