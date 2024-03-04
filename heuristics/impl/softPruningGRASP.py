import argparse
import time
from heuristics.impl.RandomSearch import RandomSearch
from predictor.estimators.estimator import Estimator
from heuristics.impl.GRASP import GRASP
from heuristics.heuristic import Heuristic
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
from domain.solution import Solution
import copy
import random
from utils.abstractSolutionsSaver import SolutionsSaver
from directives_impact_analyzer.directivesImpactAnalyzer import DirectivesImpactAnalyzer
from directives_impact_analyzer.estimatorBasedDirectivesImpactAnalyzer import EstimatorBasedDirectivesImpactAnalyzer


class SoftPruningGRASP(GRASP):
    
    def __init__(self,filesDict,model:Estimator,timeSpentTraining=0,timeLimit=43200,
                trainTime = 7200, solutionSaver:SolutionsSaver = None,seed=None,
                RCLSynthesisInterval = None, designTool = 'vitis', directivesImpactAnalyzer:DirectivesImpactAnalyzer=None):
        
        super().__init__(filesDict,model,timeSpentTraining,timeLimit,trainTime, solutionSaver,seed,RCLSynthesisInterval,designTool)
        defaultDirectiveAnalzer = EstimatorBasedDirectivesImpactAnalyzer(self.estimator)
        self.directivesImpactAnalyzer = directivesImpactAnalyzer if directivesImpactAnalyzer is not None else defaultDirectiveAnalzer
        self.cutThreshold = 0.5 #take just the 50% best
        self.designTool = designTool
    def run(self):
        end = time.time()
        numberOfIterationsInThatConfiguration=[1,2,4,8,16,32,32,32,9999999999]
        configuration = 0
        iteration = 1
        while end-self.start <= self._SECONDS:
            #change prefixed solution every x iterations, x is determined by the current configuration
            if iteration % numberOfIterationsInThatConfiguration[configuration] == 0:
                solution,groupsAvailable = self._getNewPreFixedSolution(self.cutThreshold)
                configuration+=1
            if solution is None:
                print("a")
            solution = self.constructGreedyRandomizedSolution(solution,groupsAvailable)
            solution = self.localSearch(solution,groupsAvailable)
            end = time.time()
            iteration+=1
            
    def makeRCL(self,directiveGroup:str,solutionToBuild:dict,dictDir:dict):
        """
        Enters in RCL if candidate resource X latency is below
        (1+alpha)*min(resourceXlatency of all canidates)
        """
        RCL = []
        candidates = [] 
        bestResourcesXLatency = float('inf')
        #take all candidates
        for directive in dictDir[directiveGroup]:
            solutionToBuild[directiveGroup] = directive
            candidate = Solution(solutionToBuild)
            estimatedResults = self.estimator.estimateSynthesis(candidate)
            candidate.setResultsWithListOfResults(estimatedResults)
            candidates.append(candidate)
            resourcesXlatency=  candidate.results['resources'] * candidate.results['latency']
            if  resourcesXlatency < bestResourcesXLatency:
                bestResourcesXLatency = resourcesXlatency
        
        #create RCL from some or all candidates
        #RCL = {v E Vk | dv < (1 + alpha)*min(resourcesXlatency)}
        
        #v = candidate, Vk = candidates, dv = resourcesXlatency of candidate
        for candidate in candidates:
            resourcesXlatency=  candidate.results['resources'] * candidate.results['latency']
            if  resourcesXlatency < (1+self.alpha)*bestResourcesXLatency:
                #append only the directive string
                RCL.append(candidate.directives[directiveGroup])
        return RCL

    def constructGreedyRandomizedSolution(self, preSolution:Solution, groupsAvailable:list):
        solutionToBuild = preSolution.directives
        constructedSolution = Solution(solutionToBuild)
        dictDirCopy = copy.deepcopy(self.dictDir)
        random.shuffle(groupsAvailable)
        for count,directiveGroup in enumerate(groupsAvailable):
            RCL = self.makeRCL(directiveGroup,solutionToBuild,dictDirCopy)
            if len(RCL) != 0:
                s = random.choice(RCL)
                solutionToBuild[directiveGroup] = s
            if ((count+1) % self.RCLSynthesisInterval == 0): #count+1 just to not include 0 on the count
                #synthesis of current solution under construction and feed solution to model
                constructedSolution = Solution(solutionToBuild)
                try:
                    synthesisTimeLimit = self._SECONDS - (time.time() - self.start) 
                    self.synthesisWrapper(constructedSolution,synthesisTimeLimit,self.solutionSaver, self.designTool)
                    trainingSet = copy.deepcopy(self.solutions)
                    trainingSet.extend(self.estimatorSolutions)
                    self.estimator.trainModel(trainingSet)
                except Exception as error:
                    print(error)
                else:
                    if self.solutionSaver:
                        self.solutionSaver.save(self.solutions,'./time_stamps/timeStampGRASP')
            if s != '':
                dictDirCopy = self.removeRedundantDirectives(dictDirCopy,directiveGroup,s)
        return constructedSolution
    
    def localSearch(self,solution:Solution, groupsAvailable:list):
        neighbors = [] #in resources x latency
        
        for directiveGroup in groupsAvailable:
            neighborDirectives = copy.deepcopy(solution.directives)
            for directive in self.dictDir[directiveGroup]:
                if solution.directives[directiveGroup] != directive:
                    neighborDirectives[directiveGroup] = directive
                    neighborSolution = Solution(neighborDirectives)
                    estimatedResults = self.estimator.estimateSynthesis(neighborSolution)
                    neighborSolution.setResultsWithListOfResults(estimatedResults)
                    neighbors.append(neighborSolution)
        topNSynthesis = self.synthesizeTopNSolutions(1,neighbors)
        topSolution = None
        if topNSynthesis:
            topSolution = max(topNSynthesis,key=lambda k: k.results['resources'] * k.results['latency'])    
        return topSolution
    def _sortBestDirectiveGroups(self,results):
        directiveGroups = list(self.dictDir.keys())
        directiveGroups.sort(key=lambda group: self._sortingFunction(results,group))
        return directiveGroups
    
    def _sortingFunction(self,results,group):
        bestEstimatedLatencyPlusResources = float('-inf')
        for directive in results[group].keys():
            latencyGain   = max(0,results[group][directive]['latency']) #if negative number, then goes to 0
            resourcesGain = max(0,results[group][directive]['resources'])
            if bestEstimatedLatencyPlusResources < latencyGain+resourcesGain:
                bestEstimatedLatencyPlusResources = latencyGain+resourcesGain
        return bestEstimatedLatencyPlusResources
    
    def _getNewPreFixedSolution(self, cutThreshold):
        dictDirCopy = copy.deepcopy(self.dictDir)
        results = self.directivesImpactAnalyzer.getImpacts(dictDirCopy)
        prefixedSolution = dict.fromkeys(self.dictDir,'')
        directiveGroupsSorted = self._sortBestDirectiveGroups(results)
        topN = max(1,int(len(results)*cutThreshold)) #saturates into 1 if below 1
        badGroups = directiveGroupsSorted[topN:] #get all groups that arent at topN

        for group in badGroups: 
            #select the best estimated directive for this group
            directiveChosen = self.bestEstimatedDirectiveOfGroup(results,group)
            dictDirCopy = self.removeRedundantDirectives(dictDirCopy,group,directiveChosen)
            results = self.directivesImpactAnalyzer.getImpacts(dictDirCopy)
            prefixedSolution[group] = directiveChosen
        groupsNotFixated = directiveGroupsSorted[:topN]
        return Solution(prefixedSolution),groupsNotFixated 
    
    def bestEstimatedDirectiveOfGroup(self,results, group):
        bestEstimatedDirective = ''
        bestMinimunIncrease = float('-inf')
        for directive in results[group].keys():
            latencyIncrease   = results[group][directive]['latency'] #between 0 and 1 if it reduced latency
            resourceIncrease = results[group][directive]['resources'] #between 0 and 1 if it reduced resources
            minimunIncrease = min(latencyIncrease,resourceIncrease) 
            if bestMinimunIncrease < minimunIncrease:
                bestEstimatedDirective = directive
                bestMinimunIncrease = minimunIncrease
        return bestEstimatedDirective  
