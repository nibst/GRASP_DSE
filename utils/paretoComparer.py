import copy
from typing import List
from domain.solution import Solution
from utils.abstractHeuristicComparer import HeuristicComparer
from heuristics.heuristic import Heuristic
class ParetoComparer(HeuristicComparer):

    def __init__(self,metric1,metric2):
        """
        need two metrics to decide what is in pareto metric1 X metric2
        """
        self.metric1 = metric1
        self.metric2 = metric2
    def compare(self, solutions1: List[Solution], solutions2: List[Solution]):
        """
        return percentage of paretos in solutions1 relative 
        to the total of paretos in solutions2 + solutions1
        i.e len(paretos1)/len(totalNumberOfParetos)
        """
        paretos1 = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions=solutions1)
        paretos2 = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions=solutions2)
        
        #join paretos1 and paretos2
        paretosJoint:list = copy.deepcopy(paretos1)
        paretosJoint.extend(paretos2)
        #take paretos of the junction of paretos1 and paretos2
        paretosOfPaertosJoint = Heuristic.paretoSolutions(self.metric1,self.metric2,paretosJoint)
        intersection  = self.__intersect(paretos1,paretosOfPaertosJoint)
        intersectionLenght = len(intersection)
        totalNumberOfParetos = len(paretosOfPaertosJoint)
        return intersectionLenght/totalNumberOfParetos

    def __intersect(self,solutions1:list,solutions2:list):
        """
        returns the solutions in solutions1 that intersect with solutions2
        the intersection takes in account the results in self.metric1 and self.metric2
        """
        intersection = []
        for solution1 in solutions1:
            for solution2 in solutions2:
                try:
                    if solution1.resultados[self.metric1] == solution2.resultados[self.metric1] \
                    and solution1.resultados[self.metric2] == solution2.resultados[self.metric2]:
                        intersection.append(solution1)
                except:
                    if solution1.results[self.metric1] == solution2.results[self.metric1] \
                    and solution1.results[self.metric2] == solution2.results[self.metric2]:
                        intersection.append(solution1)
        return intersection