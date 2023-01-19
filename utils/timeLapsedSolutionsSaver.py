import pickle
import time
from typing import List
from domain.solution import Solution
from heuristics.heuristic import Heuristic

class TimeLapsedSolutionsSaver():
    def __init__(self,saveInterval=None):
        self.saveInterval = saveInterval
        self.solutions = []
        self.numSaves = 0
        self.start = time.time()

    def save(self,solutions:List[Solution],savePath):
        #save all current solutions 
        self.solutions.append(solutions)
        if self.saveInterval:
            if (time.time() - self.start)/self.saveInterval >= self.numSaves + 1:
                self.__writeToFile(f'{savePath}{self.numSaves}')
                self.numSaves+=1

    def __writeToFile(self,filePath):
        with open(filePath, 'wb') as solutionsFile:
            pickle.dump(self.solutions, solutionsFile)