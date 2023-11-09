
import copy
import random
import time
from random import randint

import numpy as np
from numpy.random import choice as np_choice

from domain.solution import Solution
from heuristics.heuristic import Heuristic
from heuristics.impl.RandomSearch import RandomSearch
from predictor.estimators.estimator import Estimator
from utils.abstractSolutionsSaver import SolutionsSaver

"""
Each node will be a 'directive group' like: 'pipeline label0', 'unroll label1', 'loop_merge label0', ...
Inside each node there is differents directives to choose from. 
For example, in node 'pipeline label0' we can have 2 possible directives: None or set_directive_pipeline "label0"

Use estimation model for distances? And just synthesize final path? Recalculate all distances each n times, cause estimator 
may be more accurate

calculate pheromones for each directive in each node ("atributte" in schafer paper), then do some calculation to add pheromone to edges?

"""
class AntColony(Heuristic):

    def __init__(self,filesDict,model:Estimator, n_ants, evaporationRate, alpha=1, beta=1,timeLimit=43200,trainTime = 7200, solutionSaver:SolutionsSaver = None,seed=None ):
        """
        Args:
            n_ants (int): Number of ants running per iteration
            evaporationRate (float): Rate it which pheromone decays. The pheromone value is multiplied by evaporationRate, so 0.95 will lead to evaporation, 0.5 to much faster evaporation.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        super().__init__(filesDict)
        self.TRAIN_TIME = trainTime 
        self.SECONDS = timeLimit
        self.start = time.time()
        self.estimator = model
        self.solutionSaver = solutionSaver
        if not self.estimator.isTrained():
            sample = RandomSearch(filesDict,self.TRAIN_TIME,solutionSaver=solutionSaver)
            try:
                self.estimator.trainModel(sample.solutions)
            except Exception as error:
                print(error)
        self.estimatorSolutions = self.estimator.processor.dataset
        self.distances  = self.__initializeDistances()
        initialPheromone = 0.25
        self.pheromones = self.__initializePheromones(initialPheromone)
        self.n_ants = n_ants
        self.evaporationRate = evaporationRate
        self.alpha = alpha
        self.beta = beta
        self.areaWeight = [0.9,0.5,0.1] #it changes during heuristic
        self.latencyWeight = [0.1,0.5,0.9] #it changes during heuristic
        self.weightIndex = 0
        

        self.initalization()
    

    def run(self):
        end = time.time()

        while end-self.start <= self.SECONDS:
            #change of weights of cost function
            if end-self.start >= self.SECONDS/3:
                self.weightIndex = 1
            if end-self.start >= 2*self.SECONDS/3:
                self.weightIndex = 2
                
            directiveGroups = list(self.dictDir.keys()) 
            random.shuffle(directiveGroups)
            ants = []
            for i in range(self.n_ants):
                ant = dict.fromkeys(self.dictDir,'')
                for directiveGroup in directiveGroups:
                    ant[directiveGroup] = self.dictDir[directiveGroup][self.pickMove(directiveGroup)]
                ant = Solution(ant)
                estimatedResults = self.estimator.estimateSynthesis(ant)
                ant.setresults(estimatedResults)  
                ants.append(ant)

            synthesisTimeLimit = self.SECONDS - (time.time() - self.start)#totalTimeAvailable - timePassed
            topAnt = min(ants,key=self.costFunction)
            try:
                self.synthesisWrapper(topAnt,synthesisTimeLimit,self.solutionSaver)
                print(topAnt.results)
            except Exception as error:
                print(error)
            else:
                if self.solutionSaver:
                    self.solutionSaver.save(self.solutions,'./time_stamps/timeStampACO')
            
            trainingSet = copy.deepcopy(self.solutions)
            trainingSet.extend(self.estimatorSolutions)   
            try:
                self.estimator.trainModel(trainingSet)
            except Exception as error:
                print(error)
            if time.time()-self.start >= self.SECONDS:
                break
            
            directivesCosts = self.computeDirectivesCosts(ants)
            epsilon = self.computeEpsilon(directivesCosts)
            self.updatePheromone(epsilon)
            end = time.time()   

    def __initializeDistances(self):
        """all distances are infinite and are instanciated during path generation"""
        distances = {}
        for directiveGroup1 in self.dictDir:
            distances[directiveGroup1] = {}
            destinationDirectiveGroup = distances[directiveGroup1]
            for directiveGroup2 in self.dictDir:
                destinationDirectiveGroup[directiveGroup2] = np.inf
        return distances
    
    def distanceBetweenTwoNodes(self,node1:dict,node2:str):
        """
        TODO: each node has directives that can be applied. How do i calculate distance?
        need to decide 1 directive for node1 and test it to all directives of node2?
        or should I take all possible combinations of directives in node1 and node2?
        """

    def initalization(self):
        ants = self.initializeAnts(self.n_ants)
        directivesCosts = self.computeDirectivesCosts(ants)
        epsilon = self.computeEpsilon(directivesCosts)
        self.updatePheromone(epsilon)

    def initializeAnts(self, numberOfAnts:int):
        """
        Return 
            ants (list of dict): N ants, initialized
        """
        ants = []
        controlTree = {} #for generating non repeating permutations
        for i in range(numberOfAnts):
            ant = self.__generateRandomAnt(controlTree)
            solution = Solution(ant)
            estimatedResults = self.estimator.estimateSynthesis(solution)
            solution.setresults(estimatedResults)
            ants.append(solution)
        return ants
    
    def __generateRandomAnt(self,controlTree):
        maxRetriesPermutation = 1000#for not looping inifinitely if all permutations are already achieved
        permutationRetryCount = 0
        ant = self.generateRandomPermutation(controlTree)
        while ant == None:
            ant = self.generateRandomPermutation(controlTree)
            permutationRetryCount += 1
            if permutationRetryCount >= maxRetriesPermutation:
                break 
        return ant

    def computeDirectivesCosts(self,ants):
        """
        It can now happen that multiple ants have used the exact same attribute for
        a given operation. In this case, ε is calculates as the average of
        all the cost functions as follows: ε = 1/C = 1/(avg(Ci, Cj)).
        """
        #get max cost
        maxCost = -np.inf
        for ant in ants:
            cost = self.costFunction(ant)
            if cost>=maxCost:
                maxCost = cost
        #directivesCost will be dictionary of directives groups, and each value (group of directives) 
        # will be a dictionaries Ex: {directiveGroup1:{directive1:cost1,directive2:cost2}}
        directivesCosts = self.__initializeDirectivesCosts(maxCost)
        for directiveGroup in self.dictDir:
            self.__computeCostOfEachDirectiveInGroup(ants,directiveGroup,directivesCosts)
        return directivesCosts

    def __initializeDirectivesCosts(self,initialCost):
        directivesCost = dict.fromkeys(self.dictDir,'')
        for directiveGroup in self.dictDir:
            directivesCost[directiveGroup] = dict.fromkeys(self.dictDir[directiveGroup],initialCost)
        return directivesCost

    def __computeCostOfEachDirectiveInGroup(self,ants,directiveGroup,directivesCosts):
        for directive in self.dictDir[directiveGroup]:
            allCostsOfDirective = [] #list of costs of this directive, can be empty if no ant chooses this directive
            for ant in ants:
                if ant.directives[directiveGroup] == directive:
                    allCostsOfDirective.append(self.costFunction(ant))
            if allCostsOfDirective: #list not empty
                directivesCosts[directiveGroup][directive] = np.mean(allCostsOfDirective)
        
    def computeEpsilon(self,directivesCosts):
        """
        Args:
            directivesCosts (dict of dicts): All directives costs
        """
        epsilon = copy.deepcopy(directivesCosts)
        for directiveGroup in directivesCosts:
            for directive in directivesCosts[directiveGroup]:
                epsilon[directiveGroup][directive] = 1/(directivesCosts[directiveGroup][directive])
        return epsilon
                
        #ε = 1/C = 1/(avg(Ci, Cj))
    def __initializePheromones(self,initialPheromone):
        pheromones = dict.fromkeys(self.dictDir,'')
        for directiveGroup in self.dictDir:
            pheromones[directiveGroup] = dict.fromkeys(self.dictDir[directiveGroup],initialPheromone)
        return pheromones
    
    def pickMove(self,directiveGroup):
        pheromones = np.array(list(self.pheromones[directiveGroup].values()))

        row =  pheromones ** self.alpha * (self.localHeuristic() ** self.beta)

        norm_row = row / row.sum()
        move = np.random.choice(range(len(pheromones)), 1, p=norm_row)[0]
        return move
    
    def updatePheromone(self,epsilon):
        #τij(t + 1) = (1 − ρ) × τij(t) + ε 
        for directiveGroup in self.pheromones:
            for directive in self.pheromones[directiveGroup]:
                self.pheromones[directiveGroup][directive] = (1 - self.evaporationRate) * self.pheromones[directiveGroup][directive] + epsilon[directiveGroup][directive]
        
    def costFunction(self,ant:Solution):
        return self.areaWeight[self.weightIndex]*ant.results['resources']+ self.latencyWeight[self.weightIndex]*ant.results['latency']

    def localHeuristic(self):
        return 1