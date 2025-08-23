import copy
import time
from domain.solution import Solution
from heuristics.heuristic import Heuristic


class LocalSearch(Heuristic):
    def __init__(self, 
                 files_dict, 
                 estimator, 
                 solution_saver = None, 
                 design_tool = 'vitis', 
                 time_limit = 14400, 
                 explore_target_period = False,
                ):
        super().__init__(files_dict)
        self.estimator = estimator
        self.estimator_solutions = copy.deepcopy(self.estimator.processor.dataset)
        self.solution_saver = solution_saver
        self.design_tool = design_tool
        self.time_limit = time_limit
        self.start_time = time.time()
        self.explore_target_period = explore_target_period
        if not self.explore_target_period:
            self.exploration_knobs.pop('period', None)

    def run(self, solution: Solution):
        neighbors = self._generate_neighbors(solution)
        top_solutions = self._synthesize_top_n_solutions(1, neighbors)
        return max(top_solutions, key=lambda s:self.get_results_latency_product(s), default=None)

    def _generate_neighbors(self, solution: Solution):
        neighbors = [] #in resources x latency
        for exploration_group in self.exploration_knobs.keys():
            neighbor_directives = copy.deepcopy(solution.directives)
            if self.explore_target_period:
                neighbor_directives['period'] = solution.period
            for knob_option in self.exploration_knobs[exploration_group]:
                # itself shouldnt be considered as a neighbor
                if self._matches_selected_option(solution, exploration_group, knob_option):
                    continue
                neighbor_directives[exploration_group] = knob_option
                neighbor = Solution(neighbor_directives)
                estimated_results = self.estimator.estimateSynthesis(neighbor)
                neighbor.set_results_with_results_list(estimated_results)
                neighbors.append(neighbor)
        return neighbors
    
    def _synthesize_top_n_solutions(self, n, solutions):
        #synthesize top n solutions in the solutions list
        #sort the solutions in ascending order of resource X latency
        solutions_sorted = sorted(solutions,key=lambda k: self.get_results_latency_product(k))
        synthesis_count = 0
        top_n_synthesis = []
        for solution in solutions_sorted:
            try:
                synthesis_time_limit = self.time_limit - (time.time() - self.start_time)#totalTimeAvailable - timePassed
                self.synthesisWrapper(solution,synthesis_time_limit,self.solution_saver,self.design_tool)
            except Exception as error:
                print(error)
            else:
                if self.solution_saver:
                    self.solution_saver.save(self.solutions,'./time_stamps/timeStampGRASP')
                synthesis_count+=1
                top_n_synthesis.append(solution)
                if synthesis_count == n:
                    break
        training_set = copy.deepcopy(self.solutions)
        training_set.extend(self.estimator_solutions)  
        try:
            self.estimator.trainModel(training_set)
        except Exception as error:
            print(error)
        return top_n_synthesis

    def _matches_selected_option(self, solution, exploration_group, knob_option):
        if exploration_group == 'period':
            return solution.period == knob_option
        else:
            return solution.directives[exploration_group] == knob_option