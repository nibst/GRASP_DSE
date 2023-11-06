from abc import ABC, abstractmethod
from random import randint
import re
from domain.solution import Solution
import copy
from utils.Script_tcl import generateScript
import utils.readDirectivesFile as readDirectivesFile
from pathlib import Path
from exceptions.timeExceededException import TimeExceededException


class DesignTool(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def runSynthesis(self,timeLimit = None):
        """
        Call high level synthesis tool, respecting the time limit constrainnt
        """
        pass

    @abstractmethod
    def getSynthesisBRAMUsageFromFile(self, filePath) -> int:
        """
        Return the number of BRAMs used, according to the synthesis result in the file located in 'filePath'
        """
        pass 

    @abstractmethod
    def getSynthesisDSPUsageFromFile(self, filePath) -> int:
        """
        Return the number of DSPs used, according to the synthesis result in the file located in 'filePath'
        """
        pass
    
    @abstractmethod
    def getSynthesisFFUsageFromFile(self, filePath) -> int:
        """
        Return the number of FFs used, according to the synthesis result in the file located in 'filePath'
        """
        pass
    
    @abstractmethod
    def getSynthesisLUTUsageFromFile(self, filePath) -> int:
        """
        Return the number of LUTs used, according to the synthesis result in the file located in 'filePath'
        """
        pass

    @abstractmethod
    def getSynthesisLatencyFromFile(self, filePath) -> int:
        """
        Return the latency of the design, according to the synthesis result in the file located in 'filePath'
        """
        pass