
import copy
import os
import pickle
from typing import List
from domain.solution import Solution
from heuristics.heuristic import Heuristic
from utils.plotMaker import PlotMaker
from utils.abstractHeuristicComparer import HeuristicComparer
from utils.ADRS import ADRS

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
    def plotParetosFrontSize(plotMaker:PlotMaker,solutions1:List[List[Solution]],solutions2:List[List[Solution]],label, saveInterval):
        
        x = []
        y = []
        metrics = ['resources','latency']
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(solutions1)):
            paretos1 = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions1[i])
            paretos2 = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions2[i])
            #join paretos1 and paretos2
            paretosJoint:list = copy.deepcopy(paretos1)
            paretosJoint.extend(paretos2)
            paretosOfParetosJoint = Heuristic.paretoSolutions(metrics[0],metrics[1],paretosJoint)
            y.append(len(paretosOfParetosJoint))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label,'green')
    @staticmethod
    def bestADP(solutions:List[Solution]):

        metrics = ['resources','latency']
        if len(solutions) == 0:
            return None
        ADPs = list(map(lambda x: x.results[metrics[0]] * x.results[metrics[1]], solutions))
        return min(ADPs)
    
    @staticmethod
    def plotAverageADP(plotMaker:PlotMaker,solutions1:List[List[Solution]],solutions2:List[List[Solution]],label,saveInterval,color=None):
        x = []
        y = []
        metrics = ['resources','latency']

        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(solutions1)):
            paretos1 = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions1[i])
            paretos2 = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions2[i])
            #join paretos1 and paretos2
            paretosJoint:list = copy.deepcopy(paretos1)
            paretosJoint.extend(paretos2)
            y.append(Graphs.averageADP(paretosJoint))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label,'green')

    @staticmethod
    def averageADP(solutions:List[Solution]):
        metrics = ['resources','latency']
        if len(solutions) == 0:
            return None
        ADPs = list(map(lambda x: x.results[metrics[0]] * x.results[metrics[1]], solutions))
        if len(ADPs) != 0:
            return sum(ADPs)/len(ADPs)
        else:
            return None 
    @staticmethod
    def plotADRS(plotMaker:PlotMaker,comparer:HeuristicComparer,referenceSet:List[Solution], approximateSet:List[List[Solution]],label, saveInterval):
        x = []
        y = []
        
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(approximateSet)):
            y.append(comparer.compare(referenceSet,approximateSet[i]))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label)

