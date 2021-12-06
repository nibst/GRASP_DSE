from abc import ABC, abstractmethod
from pathlib import Path
import readDirectivesFile

class Heuristic(ABC):


    def parsedTxt(self):
        return readDirectivesFile.fileParser(self.directivesTxt)
    #Passa para o arquivo readDirectivesFile.py o texto lido do arquivo

    @abstractmethod                         # Métodos abstratos a serem herdados e implementados
    def createSolutionsLst(self):           # pelas classes filhas, com suas especificidafes
        pass
    @abstractmethod
    def writeSolutions(self):
        pass
      
    



    
    


