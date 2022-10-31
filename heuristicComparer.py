

from abc import ABC, abstractmethod
from heuristic import Heuristic

class HeuristicComparer(ABC):

    @abstractmethod
    def compare(self,heuristic1:Heuristic,heuristic2:Heuristic):
        pass
