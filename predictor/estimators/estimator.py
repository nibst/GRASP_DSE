from abc import ABC, abstractmethod
from domain.solution import Solution
class Estimator(ABC):

    @abstractmethod
    def estimateSynthesis(self,solution:Solution): #solution é um objeto da Solution não sintetizado. Para inferencia
        pass

    @abstractmethod
    def trainModel(self,dataset):
        """
        Parameters
        ----------
        dataset : List of Solution objects
        """
        pass

    @abstractmethod
    def isTrained(self):
        pass

 
        
    
        
   
        