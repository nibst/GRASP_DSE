import copy
from utils.abstractHeuristicComparer import HeuristicComparer
from heuristics.heuristic import Heuristic
class ParetoComparer(HeuristicComparer):

    def __init__(self,metric1,metric2):
        """
        need two metrics to decide what is in pareto metric1 X metric2
        """
        self.metric1 = metric1
        self.metric2 = metric2
    def compare(self, heuristic1: Heuristic, heuristic2: Heuristic):
        """
        return percentage of paretos in solutions of heuristic1 relative 
        to the total of paretos in solutions of heuristic1 + heuristic2
        i.e len(paretos1)/len(totalNumberOfParetos)
        """
        paretos1 = heuristic1.paretoSolutions(self.metric1,self.metric2)
        paretos2 = heuristic2.paretoSolutions(self.metric1,self.metric2)
        
        #join paretos1 and paretos2
        paretosJoint = copy.deepcopy(paretos1)
        index = len(paretos1)
        for solution in paretos2.values():
            paretosJoint[index] = solution
            index+=1
        #take paretos of the junction of paretos1 and paretos2
        paretosOfPaertosJoint = heuristic1.paretoSolutions(self.metric1,self.metric2,paretosJoint)
        intersection  = self.__intersect(paretos1,paretosOfPaertosJoint)
        intersectionLenght = len(intersection)
        totalNumberOfParetos = len(paretosOfPaertosJoint)
        return intersectionLenght/totalNumberOfParetos

    def __intersect(self,solutions1:dict,solutions2:dict):
        """
        returns the solutions in solutions1 that intersect with solutions2
        the intersection takes in account the results in self.metric1 and self.metric2
        """
        intersection = []
        for solution1 in solutions1.values():
            for solution2 in solutions2.values():
                try:
                    if solution1.resultados[self.metric1] == solution2.resultados[self.metric1] \
                    and solution1.resultados[self.metric2] == solution2.resultados[self.metric2]:
                        intersection.append(solution1)
                except:
                    if solution1.results[self.metric1] == solution2.results[self.metric1] \
                    and solution1.results[self.metric2] == solution2.results[self.metric2]:
                        intersection.append(solution1)
        return intersection