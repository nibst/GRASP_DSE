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
        return proportion ([0,1]) of paretos in solutions1 relative 
        to the total of paretos in solutions2 + solutions1
        i.e len(paretos1)/len(totalNumberOfParetos)
        """
        paretos1 = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions=solutions1)
        paretos2 = Heuristic.paretoSolutions(self.metric1,self.metric2,solutions=solutions2)
        #join paretos1 and paretos2
        paretosJoint:list = copy.deepcopy(paretos1)
        paretosJoint.extend(paretos2)
        #take paretos of the junction of paretos1 and paretos2
        paretosOfParetosJoint = Heuristic.paretoSolutions(self.metric1,self.metric2,paretosJoint)
        #return proportion between 0 and 1
        return self.__calculateProportionOfParetosOnParetosJoint(paretos1,paretosOfParetosJoint)

    def __calculateProportionOfParetosOnParetosJoint(self,paretos,ParetosJoint):
        intersection  = self.__intersect(paretos,ParetosJoint)
        intersectionLenght = len(intersection)
        totalNumberOfParetos = len(ParetosJoint)
        #if paretosJoint is empty, then there isnt any design space to begin with.
        #so, paretos is empty too, then (paretos and ParetosJoint) have the same paretos, which is empty
        if totalNumberOfParetos == 0:
            return 1
        else:
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