import copy
import random
import time

from domain.solution import Solution
from heuristics.heuristic import Heuristic


class GreedySolutionConstructor(Heuristic):
    def __init__(self, files_dict, 
                 estimator, 
                 solution_saver = None, 
                 design_tool = 'vitis', 
                 time_limit = 14400, 
                 rcl_synthesis_interval = 8, 
                 explore_target_period = False,
                 period_exploration_index = 0,
                ):
        super().__init__(files_dict)

        self.estimator = estimator
        self.estimator_solutions = copy.deepcopy(self.estimator.processor.dataset)
        self.solution_saver = solution_saver
        self.design_tool = design_tool
        self.time_limit = time_limit
        self.start_time = time.time()
        self.rcl_synthesis_interval = rcl_synthesis_interval
        self.explore_target_period = explore_target_period
        self.period_exploration_index = period_exploration_index
        self.alpha = 0.7
        if not self.explore_target_period:
            self.exploration_knobs.pop('period', None)

    def run(self):
        solution_blueprint = dict.fromkeys(self.exploration_knobs, '')
        exploration_knobs_copy = copy.deepcopy(self.exploration_knobs)
        shuffled_exploration_knobs = list(exploration_knobs_copy.keys())
        random.shuffle(shuffled_exploration_knobs)
        if self.explore_target_period:
            # when should the period be explored, remove existing and insert correctly
            shuffled_exploration_knobs.insert(self.period_exploration_index, 'period')
        for count, directive_group in enumerate(shuffled_exploration_knobs):
            rcl = self._make_rcl(directive_group, solution_blueprint, exploration_knobs_copy[directive_group])

            if rcl:
                selected_directive = random.choice(rcl)
                solution_blueprint[directive_group] = selected_directive

            if (count + 1) % self.rcl_synthesis_interval == 0:
                partial_solution = Solution(solution_blueprint)
                self._synthesize_partial_solution(partial_solution)
            
            if selected_directive:
                # remove all directives that are redundant with the selected directive (prunes the search space a bit
                if isinstance(selected_directive,int) and directive_group != 'period':
                    pass
                exploration_knobs_copy = self._remove_redundant_directives(exploration_knobs_copy, directive_group, selected_directive)

        return Solution(solution_blueprint)

    def _make_rcl(self, exploration_group, solution_blueprint, exploration_options):
        """
        Enters in RCL if candidate resource X latency is below
        (1+alpha)*min(resourceXlatency of all canidates)
        """
        rcl = []
        candidates = [] 
        best_resource_latency_product = float('inf')
        #take estimated results of all candidates, as well as the best estimated result
        for option in exploration_options:
            solution_blueprint[exploration_group] = option
            candidate = Solution(solution_blueprint)
            estimated_results = self.estimator.estimateSynthesis(candidate)
            candidate.set_results_with_results_list(estimated_results)
            candidates.append(candidate)
            resource_latency_product =  self.get_results_latency_product(candidate)
            if  resource_latency_product < best_resource_latency_product:
                best_resource_latency_product = resource_latency_product
        
        #create RCL from some or all candidates
        #RCL = {v E Vk | dv < (1 + alpha)*min(resource_latency_product)}
        
        #v = candidate, Vk = candidates, dv = resource_latency_product of candidate
        for candidate in candidates:
            resource_latency_product=  self.get_results_latency_product(candidate)
            if  resource_latency_product < (1+self.alpha)*best_resource_latency_product:
                if exploration_group ==  'period':
                    rcl.append(candidate.period)
                else:
                    #append only the directive string
                    rcl.append(candidate.directives[exploration_group])
        return rcl

    def _synthesize_partial_solution(self, partial_solution):
        try :
            synthesis_time_limit = self.time_limit - (time.time() - self.start_time) 
            self.synthesisWrapper(partial_solution,synthesis_time_limit,self.solution_saver, self.design_tool)
            training_set = copy.deepcopy(self.solutions)
            training_set.extend(self.estimator_solutions)
            self.estimator.trainModel(training_set)
        except Exception as e:
            print(f"Error during synthesis: {e}")
        else:
            if self.solution_saver:
                self.solution_saver.save(self.solutions,'./time_stamps/timeStampGRASP')

        

    def _remove_redundant_directives(self, exploration_knobs, directive_group, selected_directive):
        # remove all directives that are redundant with the selected directive
        # this only considers the current selected directive 
        partial_solution = Solution(dict.fromkeys(exploration_knobs,''))
        partial_solution.directives[directive_group] = selected_directive
        new_exploration_knobs = copy.deepcopy(exploration_knobs)
        for group in exploration_knobs.keys():
            if group is not directive_group and group != 'period':
                for directive in exploration_knobs[group]:
                    partial_solution.directives[group] = directive
                    if self.isRedundantDesign(partial_solution.directives):
                        new_exploration_knobs[group].remove(directive)
                    partial_solution.directives[group] = ''
        return new_exploration_knobs