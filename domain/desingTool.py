from abc import ABC, abstractmethod
from domain.solution import Solution

class DesignTool(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def runSynthesis(self,solution: Solution, timeLimit = None):
        """
        Call high level synthesis tool, respecting the time limit constrainnt
        """
        pass

