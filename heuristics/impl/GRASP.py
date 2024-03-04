import argparse
import time
from heuristics.impl.RandomSearch import RandomSearch
from predictor.estimators.estimator import Estimator
from heuristics.heuristic import Heuristic
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
from domain.solution import Solution
from utils.Script_tcl import generateScript
import copy
import random
from utils.abstractSolutionsSaver import SolutionsSaver


class GRASP(Heuristic):
    
    
    def __init__(self,filesDict,model:Estimator,timeSpentTraining=0,timeLimit=43200,trainTime = 7200, solutionSaver:SolutionsSaver = None,seed=None,RCLSynthesisInterval = None, desingTool='vitis'):
        super().__init__(filesDict)
        self.desingTool = desingTool
        self.TRAIN_TIME = trainTime #3
        self._SECONDS = timeLimit
        self.alpha = 0.7
        self.start = time.time()
        self.estimator = model
        if not self.estimator.isTrained():
            sample = RandomSearch(filesDict,self.TRAIN_TIME,solutionSaver=solutionSaver)
            try:
                self.estimator.trainModel(sample.solutions)
            except Exception as error:
                print(error)
        self.estimatorSolutions = copy.deepcopy(self.estimator.processor.dataset)
        
        random.seed(seed)        
        self.solutionSaver = solutionSaver#every 'x' time, save solutions in a file
        if RCLSynthesisInterval is None:
            self.RCLSynthesisInterval = self.__calculateRCLSynthesisInterval(timeSpentTraining)
        else:
            self.RCLSynthesisInterval = RCLSynthesisInterval
            if RCLSynthesisInterval == 0:
                self.RCLSynthesisInterval = float('inf')
       
    def __calculateRCLSynthesisInterval(self,timeTraining):
        longAverageSynthesisTime = 20 #minutes
        shortAverageSynthesisTime = 10
        intervalUsedForLongTime = len(self.dictDir.keys()) #never synthesize partial solution, only the final constructed solution
        intervalUsedForMediumTime = 8 #synthesizes every 8 partial solutions
        intervalUsedForShortTime = 2 #synthesizes every 2 partial solutions
        minutesTraining = timeTraining/60
        if len(self.estimator.results) == 0:
            return intervalUsedForLongTime
        #less than 10
        if minutesTraining/len(self.estimator.results) < shortAverageSynthesisTime:
            return intervalUsedForShortTime
        #longer than 20
        elif minutesTraining/len(self.estimator.results) >longAverageSynthesisTime:
            return intervalUsedForLongTime
        #between 10 and 20
        else:
            return intervalUsedForMediumTime

    def run(self):
        """
        procedure GRASP(Max Iterations,Seed)
            1 Read Input();
            2 for k = 1,...,Max Iterations do
                3 Solution ← Greedy Randomized Construction(Seed);
                4 if Solution is not feasible then
                    5 Solution ← Repair(Solution);
                6 end;
                8 Update Solution(Solution,Best Solution);
            9 end;
            10 return Best Solution;
        end GRASP.

        """
        end = time.time()
        #for i in range(iterations):
        while end-self.start <= self._SECONDS:
            solution = self.constructGreedyRandomizedSolution()
            solution = self.localSearch(solution)
            end = time.time()

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

    
    def constructGreedyRandomizedSolution(self):
        """
        procedure Greedy Randomized Construction(Seed)
            1 Solution ← /0;
            2 Initialize the set of candidate elements;
            3 Evaluate the incremental costs of the candidate elements;
            4 while there exists at least one candidate element do
                5 Build the restricted candidate list (RCL);
                6 Select an element s from the RCL at random;
                7 Solution ← Solution ∪ {s};
                8 Update the set of candidate elements;
                9 Reevaluate the incremental costs;
            10 end;
            11 return Solution;
        end Greedy Randomized Construction.
        """
        solutionToBuild = dict.fromkeys(self.dictDir,'') #Cria um dicionário 'diretivas' a partir do 'dictDir' mas 
                                                        #mantendo apenas os títulos das diretivas - seu valores são
                                                        #trocados por ''
        directiveGroups = list(self.dictDir.keys()) 
        dictDirCopy = copy.deepcopy(self.dictDir)
        random.shuffle(directiveGroups)
        for count,directiveGroup in enumerate(directiveGroups):
            RCL = self.makeRCL(directiveGroup,solutionToBuild,dictDirCopy)
            if len(RCL) != 0:
                s = random.choice(RCL)
                solutionToBuild[directiveGroup] = s
            if ((count+1) % self.RCLSynthesisInterval == 0): #count+1 just to not include 0 on the count
                #synthesis of current solution under construction and feed solution to model
                constructedSolution = Solution(solutionToBuild)
                try:
                    synthesisTimeLimit = self._SECONDS - (time.time() - self.start) 
                    self.synthesisWrapper(constructedSolution,synthesisTimeLimit,self.solutionSaver, self.desingTool)
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

    def removeRedundantDirectives(self,dictDir:dict,directiveGroup,directive):
        solution = dict.fromkeys(self.dictDir,'')
        newDict = copy.deepcopy(dictDir)
        solution[directiveGroup] = directive
        for group in dictDir.keys():
            if group is not directiveGroup:
                for dir in dictDir[group]:
                    solution[group] = dir
                    if self.isRedundantDesign(solution):
                        newDict[group].remove(dir)
                    solution[group] = ''
        return newDict


    def localSearch(self,solution:Solution):
        neighbors = [] #in resources x latency
        
        for directiveGroup in self.dictDir.keys():
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
    
    def synthesizeTopNSolutions(self,n:int,solutions:list):
        #synthesize top n solutions in the solutions list
        solutionsSorted = sorted(solutions,key=lambda k: k.results['resources'] * k.results['latency']) #sort in ascending order of resource X latency
        synthesisCount = 0
        topNSynthesis = []
        i = 0
        while i < len(solutionsSorted):
            try:
                synthesisTimeLimit = self._SECONDS - (time.time() - self.start)#totalTimeAvailable - timePassed
                self.synthesisWrapper(solutionsSorted[i],synthesisTimeLimit,self.solutionSaver,self.desingTool)
            except Exception as error:
                print(error)
            else:
                if self.solutionSaver:
                    self.solutionSaver.save(self.solutions,'./time_stamps/timeStampGRASP')
                synthesisCount+=1
                topNSynthesis.append(solutionsSorted[i])
                if synthesisCount == n:
                    break
            i+=1
        trainingSet = copy.deepcopy(self.solutions)
        trainingSet.extend(self.estimatorSolutions)    
        try:
            self.estimator.trainModel(trainingSet)
        except Exception as error:
            print(error)
        return topNSynthesis

        
