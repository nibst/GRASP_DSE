
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
    def plotParetoPercentage(plotMaker:PlotMaker,comparer:HeuristicComparer,solutions1:List[List[Solution]],reference_sey_by_timestamp:List[List[Solution]],label, saveInterval,linewidth=None):
        x = []
        y = []
        
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(solutions1)):
            y.append(comparer.compare(solutions1[i],reference_sey_by_timestamp[i]))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label,linewidth=linewidth)
    @staticmethod
    def plotADP(plotMaker:PlotMaker,listOfSolutionsList:List[List[Solution]],label,saveInterval,linewidth=None):
        x = []
        y = []
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i,solutions in enumerate(listOfSolutionsList):
            y.append(Graphs.bestADP(solutions))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label,linewidth=linewidth)
    @staticmethod
    def plotParetosFrontSize(plotMaker:PlotMaker,solutions:List[List[Solution]],label, saveInterval):
        
        x = []
        y = []
        metrics = ['resources','latency']
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(solutions)):
            paretos = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions[i])
            y.append(len(paretos))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label,'red')
    @staticmethod
    def bestADP(solutions:List[Solution]):

        metrics = ['resources','latency']
        if len(solutions) == 0:
            return None
        ADPs = list(map(lambda x: x.results[metrics[0]] * x.results[metrics[1]], solutions))
        return min(ADPs)
    
    @staticmethod
    def plotAverageADP(plotMaker:PlotMaker,solutions,label,saveInterval,color=None):
        x = []
        y = []
        metrics = ['resources','latency']

        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(solutions)):
            paretos = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions[i])
            y.append(Graphs.averageADP(paretos))
            x.append(saveInterval*(i+1))
        plotMaker.plot(x,y,label,'red')

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
    def plot_solutions(plot_maker:PlotMaker,solutions:List[Solution], label):
        metrics = ['resources','latency']
        x = []
        y = []
        for solution in solutions:
            x.append(solution.results[metrics[0]])
            y.append(solution.results[metrics[1]])
        plot_maker.ylim(0, max(y))
        plot_maker.scatter_plot(x,y,label)

    def plot_paretos(plot_maker:PlotMaker,solutions:List[Solution], my_solutions = [], 
                     only_default_freq=False, only_non_default_freq=False,
                     label='', main_color='blue',secondary_color='red',main_opacity=1, secondary_opacity=1 ,marker='o', secondary_marker='^'):    
        metrics = ['resources','time_latency']
        x = []
        y = []
        x_diff = []
        y_diff = []
        paretos = Heuristic.paretoSolutions(metrics[0],metrics[1],solutions=solutions)
        for solution in paretos:
            if solution.period != 8:
                x_diff.append(solution.results[metrics[0]])
                y_diff.append(solution.results[metrics[1]])
            else :
                x.append(solution.results[metrics[0]])
                y.append(solution.results[metrics[1]])
        combined_y = y + y_diff
        if len(combined_y) == 0:
            combined_y = [0]
        if not only_non_default_freq:
            plot_maker.scatter_plot(x, y, color=main_color, marker=marker, size=80, label=label,opacity=main_opacity)
        if len(x_diff) > 0 and len(y_diff) > 0 and not only_default_freq:
            plot_maker.scatter_plot(x_diff, y_diff, color=secondary_color, marker=secondary_marker, size=80,label=label, opacity=secondary_opacity)

    
    def plot_solutions_intersections(plot_maker:PlotMaker,solutions:List[Solution], my_solutions:List[Solution], metrics, color='blue', marker='o', label=''):
        intersection = []
        for solution1 in my_solutions:
            for solution2 in solutions:
                if solution1.results[metrics[0]] == solution2.results[metrics[0]] \
                and solution1.results[metrics[1]] == solution2.results[metrics[1]]:
                    intersection.append(solution1)
        if len(intersection) > 0:
            intersection_x = [sol.results[metrics[0]] for sol in intersection]
            intersection_y = [sol.results[metrics[1]] for sol in intersection]
            plot_maker.scatter_plot(intersection_x, intersection_y, color=color, marker=marker, size=80, opacity=1, label=label)

    def plotADRS(plotMaker:PlotMaker,comparer:HeuristicComparer,referenceSet:List[Solution], approximateSet:List[List[Solution]],label, saveInterval,linewidth=None):
        x = []
        y = []
        
        saveInterval = saveInterval/60 #convert seconds to minutes
        for i in range(len(approximateSet)):
            y.append(comparer.compare(referenceSet,approximateSet[i]))
            x.append(saveInterval*(i+1))
        bot,top = plotMaker.get_ylim()
        max_y = max(filter(lambda val: val is not None, y))
        if top < max_y:
            plotMaker.ylim(bot, max_y + max_y/10)
        plotMaker.plot(x,y,label,linewidth=linewidth)
    @staticmethod
    def plotAllBenchmarksSummarized():
        pass
