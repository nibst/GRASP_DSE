
import os
import pickle
from typing import List
from domain.solution import Solution
from utils.plotMaker import PlotMaker
from utils.abstractHeuristicComparer import HeuristicComparer
class Graphs:
    @staticmethod
    def __getOrderedSavesPaths(path):
        dirList:list = os.listdir(path)
        dirList.sort(key=lambda x : int(x[ len(x) - 1]))
        relativePaths = list(map(lambda x: path+x, dirList))
        return relativePaths
    @staticmethod
    def __saveFilesToSolutionsList(paths:list):
        #TODO, timestamp of random search is different
        listOfSolutionsList:List[List[Solution]] = []
        for path in paths:
            with open(path,'rb') as file:
                solutions = pickle.load(file)
            listOfSolutionsList.append(solutions)
        return listOfSolutionsList

    def pathToListsOfSolutions(path):
        orderedPaths = Graphs.__getOrderedSavesPaths(path)
        return Graphs.__saveFilesToSolutionsList(orderedPaths)
    @staticmethod
    def plotParetoPercentage(plotMaker:PlotMaker,comparer:HeuristicComparer,solutions1:List[List[Solution]],solutions2:List[List[Solution]],label, saveInterval):
        x = []
        y = []
        
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(solutions1)):
            y.append(comparer.compare(solutions1[i],solutions2[i]))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label)
    @staticmethod
    def plotADP(plotMaker:PlotMaker,listOfSolutionsList:List[List[Solution]],label,saveInterval):
        x = []
        y = []
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i,solutions in enumerate(listOfSolutionsList):
            y.append(Graphs.bestADP(solutions))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label)
    @staticmethod
    def bestADP(solutions:List[Solution]):

        metrics = ['resources','latency']
        if len(solutions) == 0:
            return None
        ADPs = list(map(lambda x: x.results[metrics[0]] * x.results[metrics[1]], solutions))
        return min(ADPs)
