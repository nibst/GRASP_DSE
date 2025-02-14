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
            self.__extendWithOnlyNewSolutions(solutions)
        timeElapsed = time.time() - self.start
        if self.saveInterval:
            if timeElapsed >= self.saveInterval:
                self.__writeToFile(f'{savePath}{self.numSaves}')
                self.numSaves+=1
                self.start = time.time() # reset timer
                
    def __extendWithOnlyNewSolutions(self,newSetOfSolutions):
        solutionsLen = len(self.solutions)
        i=0
        if self.solutions:
            for i in range(len(newSetOfSolutions)-1,-1,-1):
                if newSetOfSolutions[i] is self.solutions[solutionsLen-1]:
                    i+=1
                    break
        self.solutions.extend(newSetOfSolutions[i:])
        
        
    def __writeToFile(self,filePath):
        with open(filePath, 'wb') as solutionsFile:
            pickle.dump(self.solutions, solutionsFile)
