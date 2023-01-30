import time
from exceptions.timeExceededException import TimeExceededException
from heuristics.impl.RandomSearch import RandomSearch
from utils.Script_tcl import generateScript
from predictor.estimators.estimatorFactory import EstimatorFactory
from heuristics.heuristic import Heuristic
from domain.solution import Solution
import copy
import random
from sklearn.model_selection import train_test_split
from typing import List
from utils.abstractSolutionsSaver import SolutionsSaver


class GA(Heuristic):

    def __init__(self,filesDict,outPath,estimatorFactory:EstimatorFactory,baseEstimator = None,timeLimit=43200,trainTime=3600,solutionSaver:SolutionsSaver = None,seed=0 ):
        super().__init__(filesDict, outPath)
        self._SECONDS = timeLimit
        self.TRAIN_TIME = trainTime
        self.populationSize = 60 #any number
        self.estimatorFactory = estimatorFactory
        self.crossoverRate = 0.8 #any number between 0 and 1
        self.mutationRate = 0.1 #any number between 0 and 1
        self.modelThreshold = 0.1
        random.seed(seed)

        self.numOfGenes = len(self.dictDir.keys())
        self.listOfKeys = list(self.dictDir.keys()) #to use numbers (indexes of list) instead of strings in the algorithm logic
        self.chaceToOverwrite = 0.5 #probability of overwritting parent with offspring if offspring dominates in one of the objectives
        self.new_model_interval = 120

        self.solutionSaver = solutionSaver
        self.start = time.time()
        #use this base estimator until next call of new predictive model
        if not baseEstimator:
            self.__new_predictive_model()
        else:
            self.estimator = baseEstimator
        self.finalPopulation = self.run()
        
        
    def run(self):
        """
        n: numero de individuos
        g: numero de gerações
        f: funcao de aptidao que quero maximizar/minimizar
        #no nosso caso f seria rodar sintese e utilizar alguma forma de analisar (seja pareto, seja alguma metrica individual, seja minimizar latXresources)
        #o1,o2 = offspring1 offspring2
        P<-aleatorios(n)
        repetir g vezes:
            P' <-  Vazio
            enquanto tam(P')<n:
                pai1,pai2 <- selecao(P)
                o1,o2 <- crossover(pai1,pai2)
                o1 <- mutation(o1)
                o2 <- mutation(o2)
                P' <- P'  U {o1,o2}
        P <- P'
        retornar top(x,P,f) #top x individuos de P
        
        #k: numero de participantes torneio
        selecao_torneio(P,f,k):
            part <- unif.aleatorio(P,k)
            return top(2,part,f)

        crossover(pai1,pai2):
            se random < prob_crossover
                o1,o2 <- troca(pai1,pai2)
            senao
                o1,o2 <- copia(pai1,pai2)
            return o1,o2

        funcao top colocará os results (o fitness de cada solucao) nas Solutions da populacao

        mutation com mutacao aleatorio do domninio
        """
        """
        maybe do something like this:
        mutation= True
        crossover =True
        if random() < self.crossOverRate:
            offspring = self.crossover(parent1,parent2)
        else:
            crossover = False
        if random() < self.mutationRate:
            offspring = self.mutation(offspring)
        else:
            mutation = False
        if crossover or mutation:
            newPopulation.extend([offspring])

        """
        generateScript(self.cFiles, self.prjFile)
        population = self.randomSample() #list of random Solutions (without their HLS results yet)
        interval = 0
         
        newPopulation = []
        parentPairs = self.selector(population)
        pairIndex = 0
        while (time.time() - self.start) < self._SECONDS:
            if self.solutionSaver:
                self.solutionSaver.save(self.solutions,'./time_stamps/timeStampGenetic')
            try:
                newParent1,newParent2 = self.__generateNextPairOfParents(parentPairs[pairIndex])
            except IndexError:
                population = self.randomSample() #list of random Solutions (without their HLS results yet)
                parentPairs = self.selector(population)
                pairIndex = 0

            newPopulation.extend([newParent1,newParent2])
            #synthesize parents that went to final pareto population 
            try:
                self.__synthesizeBothNewParents(newParent1,newParent2)
            except TimeExceededException as e:
                print(e)
                return

            if (time.time() - self.start) >= self._SECONDS:
                break
            #save all current solutions 
            if self.solutionSaver:
                self.solutionSaver.save(self.solutions,'./time_stamps/timeStampGenetic')
            pairIndex+=1
            interval+=1
            if interval % self.new_model_interval == 0:
                self.__new_predictive_model()
                        #save all current solutions 
                
        if self.solutionSaver:
            self.solutionSaver.save(self.solutions,'./time_stamps/timeStampGenetic')
        population = newPopulation
        return population

    def __generateNextPairOfParents(self,parentPair):
            parent1,parent2 = parentPair
            offspring = self.crossover(parent1,parent2)
            offspring = self.mutation(offspring)    
            estimatedResults = self.estimator.estimateSynthesis(offspring)
            offspring.setresults(estimatedResults)
            newParent1,newParent2 = self.overwriteParent(parent1,parent2,offspring)
            return (newParent1,newParent2)

    def __synthesizeBothNewParents(self,newParent1,newParent2):
            synthesisTimeLimit = self._SECONDS - (time.time() - self.start) 
            try:
                self.synthesisWrapper(newParent1,synthesisTimeLimit)
            except TimeExceededException as e:
                print(e)
                raise
            except Exception as e:
                print(e)

            synthesisTimeLimit = self._SECONDS - (time.time() - self.start)  
            try:
                self.synthesisWrapper(newParent2,synthesisTimeLimit)
            except TimeExceededException as e:
                print(e)
                raise
            except Exception as e:
                print(e) 
                
    def __new_predictive_model(self):
        #maybe create new model, as deep copy of self.estimator
        score = -1
        threshold = self.modelThreshold 
        self.estimator = self.estimatorFactory.create()
        sample = RandomSearch(self.filesDict, self.outPath,self.TRAIN_TIME,solutionSaver=self.solutionSaver)
        start = time.time()
        while score < threshold:
            try:    
                train, test = train_test_split(sample.solutions, test_size=0.2, random_state=0)
                self.estimator.trainModel(train)
                
                score = self.estimator.score(test)
                self.estimator.trainModel(sample.solutions)
            except Exception as e:
                #do nothing, just train more
                score = -1 
                print(e)            
            print(f'score: {score} ')
            #full train
            print(f'sample solutions lenght: {len(sample.solutions)}') 
            
            if score < threshold: 
                #if the time spent creating a new model is x times the TRAIN TIME, lower the threshold
                if time.time() - start >= self.TRAIN_TIME*3:
                    threshold-=0.05   
                #create more samples
                sample.run()
            #if time runs out
            if (time.time() - self.start) >= self._SECONDS:
                break
        
        for solution in sample.solutions:
            self.appendSolution(solution)
    
    def selector(self,population):
        parentsList = []
        for parent1 in population:
            #This will estimate all parents in population and pair each parent to a diferent parent
            try:
                estimatedResults = self.estimator.estimateSynthesis(parent1)
                parent1.setresults(estimatedResults)
            except Exception as e:
                print(e)
            parent2 =random.choice(population)
            while parent1 == parent2:
                parent2 =random.choice(population)
            parentsList.append(parent2)
        return list(zip(population,parentsList))
                
      
    def randomSample(self):
        controlTree = {}
        sample = []
        onePermutation = None
        i=0
        while i<(self.populationSize):
            onePermutation = self.__generateRandomPermutation(controlTree)
            if onePermutation:
                solution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste
                sample.append(solution)
                i+=1
        return sample

    def top(self,numOfTops, population:List[Solution]):

        topSolutions = [] #top "numOfTops" solutions
        for count,individual in enumerate(population):
            topSolutions.append(individual) 
            if count >= numOfTops:
                self.__removeWorstSolution(topSolutions)
        return topSolutions

    def __removeWorstSolution(self,topSolutions):
        worst = float('-inf')
        for solution in topSolutions:
            if solution.results['resources'] * solution.results['latency'] >= worst:
                worst = solution.results['resources'] * solution.results['latency']
                worstSolution = solution
        topSolutions.remove(worstSolution)

    def mutation(self,individual:Solution):
        
        if random.random() < self.mutationRate:
            geneToMutate = random.randint(0,self.numOfGenes-1)
            gene = copy.deepcopy(self.dictDir[self.listOfKeys[geneToMutate]])#copy cause we gonna modify
            gene.remove(individual.directives[self.listOfKeys[geneToMutate]]) #remove current gene value from the choices
            mutation = random.choice(gene)
            individual.directives[self.listOfKeys[geneToMutate]] = mutation
        return individual
    
    def crossover(self,parent1,parent2):
        #TODO dont know about returnming copy of parent if the crossover dont happen
        
        if random.random() < self.crossoverRate:
            cutPoint = random.choice(self.listOfKeys)
            offspringDirectives = {}
            parent = parent1
            for key in self.listOfKeys:
                if key == cutPoint:
                    parent = parent2 #swap from which parent take genes
                offspringDirectives[key] = parent.directives[key]
            offspring = Solution(offspringDirectives, self.cFiles, self.prjFile)
        else:
            offspring = copy.deepcopy(parent1)
        return offspring
    def overwriteParent(self,parent1,parent2,offspring):
        """.
        Replace one of the parents if it dominates it in all the
        objectives (area and latency). If the offspring only dominates one of the objectives, it is randomly decided if it
        substitutes one of the parents or not.
        """    
        #if offspring dominates parent1 and parent2 in all objectives, replace one of the parents randomly            
        if Heuristic.dominateInBothMetrics(offspring,parent1,'resources','latency') and Heuristic.dominateInBothMetrics(offspring,parent2,'resources','latency'):
            #replace one of the parents randomly
            if random.random() < 0.5:
                parent1 = offspring
            else:
                parent2 = offspring
            return parent1,parent2
        #if offspring dominates parent1 in all objectives, replace parent1
        elif Heuristic.dominateInBothMetrics(offspring,parent1,'resources','latency'):
            parent1 = offspring
            return parent1,parent2
        #if offspring dominates parent2 in all objectives, replace parent2
        elif Heuristic.dominateInBothMetrics(offspring,parent2,'resources','latency'):
            parent2 = offspring
            return parent1,parent2

        #if offspring dominates parent1 and parent2 in one objective, random chance to replace random parent with offspring
        elif self.__dominateAtLeastOneMetric(offspring,parent1,'resources','latency') and self.__dominateAtLeastOneMetric(offspring,parent2,'resources','latency'):
            chance = random.random()
            #int total parents have 0.5 chance to be replaced
            if chance < 0.25:
                parent1 = offspring
            if chance > 0.75:
                parent2 = offspring
            return parent1,parent2

        #if offspring dominates parent1 in one objective, random chance to replace parent1 with offspring
        if self.__dominateAtLeastOneMetric(offspring,parent1,'resources','latency'):
            if random.random() < 0.5:
                parent1 = offspring
            return parent1,parent2

        #if offspring dominates parent2 in one objective, random chance to replace parent1 with offspring
        if self.__dominateAtLeastOneMetric(offspring,parent2,'resources','latency'):
            if random.random() < 0.5:
                parent2 = offspring
            return parent1,parent2  
        
        return parent1,parent2
    
    def __dominateAtLeastOneMetric(self,Solution1,Solution2,metric1,metric2):
        #testa se a Solution1  domina a Solution2
        return ((Solution2.results[metric1]>=Solution1.results[metric1]) or (Solution2.results[metric2] >= Solution1.results[metric2]))
        
    def __generateRandomPermutation(self,controlTree:dict):
        node = controlTree
        newPermutation = {}
        isNewPermutation = False #flag para verificar se é permutacao/solucao/design repetida ou nao
        for directive in self.dictDir:              
            domainLenght = len(self.dictDir[directive])   
            randomDirective = random.randint(0,domainLenght-1)
            newPermutation[directive] = self.dictDir[directive][randomDirective] 
            if randomDirective in node:
                node = node[randomDirective]
            else:
                node[randomDirective] = {} #cria nodo
                node = node[randomDirective]
                isNewPermutation = True
        if isNewPermutation:
            return newPermutation
        else:
            #if self.__exhaustedEverySolution():
            return None
    #TODO
    def __exhaustedEverySolution(self,controlTree):
        return True

    
