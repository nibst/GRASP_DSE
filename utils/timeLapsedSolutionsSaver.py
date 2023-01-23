import copy
import pickle
import time
from typing import List
from domain.solution import Solution
from heuristics.heuristic import Heuristic
from utils.abstractSolutionsSaver import SolutionsSaver

class TimeLapsedSolutionsSaver(SolutionsSaver):
    def __init__(self,saveInterval=None):
        self.saveInterval = saveInterval
        self.numSaves = 0
        self.start = time.time()

    def save(self,solutions:List[Solution],savePath):
        #save all current solutions 
        
        timeElapsed = time.time() - self.start
        if self.saveInterval:
            if timeElapsed >= self.saveInterval:
                shallow = list(solutions)  
                self.__writeToFile(shallow,f'{savePath}{self.numSaves}')
                self.numSaves+=1
                self.start = time.time() # reset timer
                
                
    def __writeToFile(self,solutions,filePath):
        with open(filePath, 'wb') as solutionsFile:
            pickle.dump(solutions, solutionsFile)