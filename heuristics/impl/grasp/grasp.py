import copy
import time
from domain.solution import Solution
from heuristics.heuristic import Heuristic
from heuristics.impl.RandomSearch import RandomSearch
from heuristics.impl.grasp.greedy_solution_constructor import GreedySolutionConstructor
from heuristics.impl.grasp.local_search import LocalSearch
from predictor.estimators.estimator import Estimator
import os
from datetime import datetime
import pickle


class Grasp(Heuristic):
    def __init__(self, files_dict, model: Estimator, **kwargs):
        super().__init__(files_dict)
        self.design_tool = kwargs.get('design_tool', 'vitis')
        self.time_limit = kwargs.get('time_limit', 43200)
        self.alpha = kwargs.get('alpha', 0.7)
        self.start_time = time.time()
        self.estimator = model
        self.solution_saver = kwargs.get('solution_saver', None)
        self.explore_target_period = kwargs.get('explore_target_period', False)
        self.rcl_synthesis_interval = kwargs.get('rcl_synthesis_interval', None)
        self.period_exploration_index = kwargs.get('period_exploration_index', 0)

        self.estimator_solutions = copy.deepcopy(self.estimator.processor.dataset)

        if not self.explore_target_period:
            self.exploration_knobs.pop('period', None)
        # Initialize RCL synthesis interval
        if self.rcl_synthesis_interval is None:
            if self.explore_target_period:
                number_of_solutions_trained = 60 #60 for now because thats the number of solutions that I extended from dataset with period
            else:
                number_of_solutions_trained = len(self.estimator.processor.dataset)
            self.rcl_synthesis_interval = self._calculate_rcl_synthesis_interval(kwargs.get('time_spent_training', 0), number_of_solutions_trained)

    def _save_heuristic_snapshot(self):
        # Save the snapshot of the heuristic if needed
        snapshots_folder = './snapshots'
        os.makedirs(snapshots_folder, exist_ok=True)
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        snapshot_file = os.path.join(snapshots_folder, f'grasp_heuristic_snapshot_{current_time}')

        snapshot_data = {
            'design_tool': self.design_tool,
            'time_limit': self.time_limit,
            'alpha': self.alpha,
            'start_time': self.start_time,
            'state_time': time.time(),
            'estimator_solutions': self.estimator_solutions,
            'explore_target_period': self.explore_target_period,
            'rcl_synthesis_interval': self.rcl_synthesis_interval,
            'period_exploration_index': self.period_exploration_index,
            'solutions': self.solutions
        }

        with open(snapshot_file, 'wb') as f:
            pickle.dump(snapshot_data, f)
    def _calculate_rcl_synthesis_interval(self, time_training, number_of_solutions=0):
        # Average synthesis times in minutes
        long_average_synthesis_time = 20
        short_average_synthesis_time = 10

        # Intervals for synthesis
        interval_for_long_time = len(self.exploration_knobs.keys())  # Synthesize only the final constructed solution
        interval_for_medium_time = 8  # Synthesize every 8 partial solutions
        interval_for_short_time = 2  # Synthesize every 2 partial solutions

        # Calculate training time in minutes
        minutes_training = time_training / 60

        # Handle cases based on training time and estimator results
        if number_of_solutions == 0:
            return interval_for_long_time  # No results, use the longest interval

        average_training_time_per_result = minutes_training / number_of_solutions

        if average_training_time_per_result < short_average_synthesis_time:
            return interval_for_short_time  # Training time per result is short
        elif average_training_time_per_result > long_average_synthesis_time:
            return interval_for_long_time  # Training time per result is long
        else:
            return interval_for_medium_time  # Training time per result is medium

    def run(self):
        while time.time() - self.start_time <= self.time_limit:
            solution = self.construct_greedy_randomized_solution()
            solution = self.local_search(solution)
            self._save_heuristic_snapshot()
        return self.paretoSolutions("time_latency","resources",self.solutions)
    def construct_greedy_randomized_solution(self):
        time_limit = self.time_limit - (time.time() - self.start_time)
        constructor = GreedySolutionConstructor(
            self.files_dict, self.estimator, self.solution_saver, self.design_tool,
            time_limit, self.rcl_synthesis_interval, self.explore_target_period, self.period_exploration_index
        )
        constructed_solution = constructor.run()
        self.solutions.extend(constructor.solutions)
        return constructed_solution

    def local_search(self, solution: Solution):
        time_limit = self.time_limit - (time.time() - self.start_time)
        searcher = LocalSearch(
            self.files_dict, self.estimator, self.solution_saver, self.design_tool, 
            time_limit, self.explore_target_period
        )
        top_neighbor = searcher.run(solution)
        self.solutions.extend(searcher.solutions)
        return top_neighbor