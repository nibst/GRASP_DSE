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
        self.solutions = []
        self.start = time.time()

    def save(self,solutions:List[Solution],savePath):
        #save all current solutions 
        if solutions:
            self.solutions = solutions
        timeElapsed = time.time() - self.start
        if self.saveInterval:
            if timeElapsed >= self.saveInterval:
                self.__writeToFile(f'{savePath}{self.numSaves}')
                self.numSaves+=1
                self.start = time.time() # reset timer
                
                
    def __writeToFile(self,filePath):
        with open(filePath, 'wb') as solutionsFile:
            pickle.dump(self.solutions, solutionsFile)