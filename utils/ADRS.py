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
        self.lastminAdrsList = []

    def compare(self, solutions1: List[Solution], solutions2: List[Solution]):
        if len(solutions2) == 0:
            return None
        adrs = 0
        referenceParetoFrontSet = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions1)
        approximateParetoFrontSet = solutions2#Heuristic.paretoSolutions(self.metric1,self.metric2,solutions2)
        for referenceSetSolution in referenceParetoFrontSet:
            adrsList = []
            for approximateSetSolution in approximateParetoFrontSet:
                adrsList.append(self.distance(referenceSetSolution,approximateSetSolution))
            if adrsList:
                adrs += min(adrsList)
                self.lastminAdrsList.append((min(adrsList),adrsList.index(min(adrsList))))
        return 1/(len(referenceParetoFrontSet)) * adrs
    
    def distance(self,referenceSetSolution:Solution, approximateSetSolution:Solution):
        if self.metric1 == 'time_latency' or self.metric2 == 'time_latency':
            referenceSetSolution.results['time_latency'] = referenceSetSolution.results['latency'] * referenceSetSolution.period
            approximateSetSolution.results['time_latency'] = approximateSetSolution.results['latency'] * approximateSetSolution.period

        aw = approximateSetSolution.results[self.metric1]
        lw = approximateSetSolution.results[self.metric2]

        ay = referenceSetSolution.results[self.metric1]
        ly = referenceSetSolution.results[self.metric2]
        return max(abs((aw-ay)/ay) , abs((lw-ly)/ly))
