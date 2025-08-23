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
        paretosOfParetosJoint = self.__remove_duplicates(paretosOfParetosJoint)
        #return proportion between 0 and 1
        return self.__calculateProportionOfParetosOnParetosJoint(paretos1,paretosOfParetosJoint)

    def __calculateProportionOfParetosOnParetosJoint(self,paretos,paretosJoint):
        intersection  = self.__intersect(paretos,paretosJoint)
        intersectionLenght = len(intersection)
        totalNumberOfParetos = len(paretosJoint)
        #if paretosJoint is empty, then there isnt any design space to begin with.
        #so, paretos is empty too, then (paretos and paretosJoint) have the same paretos, which is empty
        if totalNumberOfParetos == 0:
            return 1
        else:
            return intersectionLenght/totalNumberOfParetos

    def __intersect(self,solutions1:list,solutions2:list):
        """
        returns the solutions in solutions1 that intersect with solutions2
        the intersection takes in account the directives and period of the solutions.
        """
        # Build a set of (directives_tuple, period) for list1
        set1 = set(
            (tuple(sorted(sol.directives.items())), sol.period)
            for sol in solutions1
        )
        # Now, for each solution in list2, check if its key is in set1
        intersection = [
            sol for sol in solutions2
            if (tuple(sorted(sol.directives.items())), sol.period) in set1
        ]
        return intersection
    
    def __remove_duplicates(self, solutions: List[Solution]) -> List[Solution]:
        """
        Removes duplicate solutions based on their directives and period.
        """
        seen = set()
        unique_solutions = []
        for sol in solutions:
            # Convert directives dict to a tuple of sorted items for hashing
            directives_tuple = tuple(sorted(sol.directives.items()))
            period = sol.period
            key = (directives_tuple, period)
            if key not in seen:
                seen.add(key)
                unique_solutions.append(sol)
        return unique_solutions
