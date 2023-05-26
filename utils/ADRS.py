import copy
from typing import List
from domain.solution import Solution
from utils.abstractHeuristicComparer import HeuristicComparer
from heuristics.heuristic import Heuristic

class ADRS(HeuristicComparer):

    def __init__(self,metric1,metric2):
        """
        need two metrics to decide what is in pareto metric1 X metric2
        """
        self.metric1 = metric1
        self.metric2 = metric2

    def compare(self, solutions1: List[Solution], solutions2: List[Solution]):
        adrs = 0
        referenceParetoFrontSet = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions1)
        approximateParetoFrontSet = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions2)
        for referenceSetSolution in referenceParetoFrontSet:
            for approximateSetSolution in approximateParetoFrontSet:
                adrs += self.distance(referenceSetSolution,approximateSetSolution)
        return 1/(len(referenceParetoFrontSet)) * adrs
    
    def distance(self,referenceSetSolution:Solution, approximateSetSolution:Solution):
        aw = approximateSetSolution.results['resources']
        lw = approximateSetSolution.results['latency']

        ay = referenceSetSolution.results['resources']
        ly = referenceSetSolution.results['latency']
        return max(abs((aw-ay)/ay) , abs((lw-ly)/ly))
