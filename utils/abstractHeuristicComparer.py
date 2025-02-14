from abc import ABC, abstractmethod
from typing import List
from domain.solution import Solution
from heuristics.heuristic import Heuristic

class HeuristicComparer(ABC):

    @abstractmethod
    def compare(self,solutions1: List[Solution], solutions2: List[Solution]):
        pass