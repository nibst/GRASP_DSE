from abc import ABC, abstractmethod
from typing import List
from domain.solution import Solution
from heuristics.heuristic import Heuristic

class SolutionsSaver(ABC):

    def save(self,solutions:List[Solution],savePath):
        pass