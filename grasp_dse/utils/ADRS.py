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
        aw = approximateSetSolution.results['resources']
        lw = approximateSetSolution.results['latency']

        ay = referenceSetSolution.results['resources']
        ly = referenceSetSolution.results['latency']
        return max(abs((aw-ay)/ay) , abs((lw-ly)/ly))
