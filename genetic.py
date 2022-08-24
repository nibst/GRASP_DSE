import time
from RandomSearch import RandomSearch
from estimator import Estimator
from heuristic import Heuristic
from solution import Solution
import copy
import random
from sklearn.model_selection import train_test_split
from typing import List

class GA(Heuristic):
    _SECONDS = 50000 #2 hour
    def __init__(self,filesDict,outPath,model:Estimator,numOfGenerations = 10):
        super().__init__(filesDict, outPath)
        self.dictDir =self.parsedTxt()
        self.numOfIndividuals = 40 #any number
        self.numOfGenes = len(self.dictDir.keys())
        self.numOfGenerations = numOfGenerations
        self.listOfKeys = list(self.dictDir.keys()) #to use numbers (indexes of list) instead of strings in the algorithm logic
        self.crossoverRate = 0.8 #any number between 0 and 1
        self.mutationRate = 0.1 #any number between 0 and 1
        self.chaceToOverwrite = 0.5 #probability of overwritting parent with offspring if offspring dominates in one of the objectives
        sample = RandomSearch(filesDict, outPath)
        self.estimator = model
        self.estimator.trainModel(sample.solutions)
        self.new_model_interval = 20
        self.threshold = -1.5
        self.createSolutionsDict()
        
        
    def createSolutionsDict(self):
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

        funcao top colocará os resultados (o fitness de cada solucao) nas Solutions da populacao

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
            new_population.extend([offspring])

        """
        random.seed(1)
        start = time.time()
        population = self.randomSample() #list of random Solutions (without their HLS results yet)
        for i in range(self.numOfGenerations):
            new_population = []
            interval = 0
            parentPairs = self.selector(population)
            while len(new_population) < self.numOfIndividuals:
                parent1,parent2 = parentPairs[interval]
                offspring = self.crossover(parent1,parent2)
                offspring = self.mutation(offspring)
                try:
                    estimatedResults = self.estimator.estimateSynthesis(offspring)
                    offspring.setResultados(estimatedResults)
                    parent1,parent2 = self.overwriteParent(parent1,parent2,offspring)
                except Exception as e:
                    print(e)
                else:
                    new_population.extend([offspring])
                if interval >= self.new_model_interval:
                    self.model=self.__new_predictive_model()
                end = time.time()
                totalTime = (end-start)
                if totalTime >= self._SECONDS:
                    return
                interval+=1
            population = new_population
            
    def __new_predictive_model(self):
        score = -2
        sample = RandomSearch(self.filesDict, self.outPath)
        while score < self.threshold:
            train, test = train_test_split(sample.solutions, test_size=0.2, random_state=0)
            self.estimator.trainModel(train)
            score = self.estimator.score(test)
            print(f'score: {score} ')
            #full train
            self.estimator.trainModel(sample.solutions)
            if score < self.threshold:    
                #create more samples
                sample.createSolutionsDict()
        for solution in sample.solutions.values():
            self.saveSolution(solution)
    
    def selector(self,population):
        copy.deepcopy(population)
        pairList = []
        for parent1 in population:
            try:
                self.synthesisWrapper(parent1)
            except Exception as e:
                print(e)
            parent2 =random.choice(population)
            while parent1 == parent2:
                parent2 =random.choice(population)
            pairList.append(parent2)
        return list(zip(population,pairList))
                
            
    def selector_tournament(self,population,numOfIndividuals):
        #tournament
        part = self.__uniformRandom(population,numOfIndividuals)
        for individual in part:
            #just synthesize solutions that have not been synthesized yet
            if None in individual.resultados.values():
                try:
                    estimatedResults = self.estimator.estimateSynthesis(individual)
                    individual.setResultados(estimatedResults)
                except Exception as e:
                    print(e)
                    
        return self.top(2,part)

    def __uniformRandom(self,population,numOfIndividuals):
        #TODO use a lib wtf
        domainLenght = len(population)
        indexes = [] # indexes of the individuals that got selected
        i = 0
        while i < numOfIndividuals:
            individualIndex = random.randint(0,domainLenght-1)
            if individualIndex not in indexes:
                indexes.append(individualIndex)
                i+=1
        part = [] #list of the population that gonna be returned
        for index in indexes:
            part.append(population[index])
        return part
            
    def randomSample(self):
        controlTree = {}
        sample = []
        onePermutation = None
        i=0
        while i<(self.numOfIndividuals):
            onePermutation = self.__generateRandomPermutation(controlTree)
            if onePermutation:
                solution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste
                sample.append(solution)
                i+=1
        return sample

    def top(self,numOfTops, population:List[Solution]):

        topSolutions = [] #top "numOfTops" solutions
        for count,individual in enumerate(population):
            if count >= numOfTops:
                self.__removeWorstSolution(topSolutions)
            topSolutions.append(individual) 
        return topSolutions

    def mutation(self,individual:Solution):
        
        if random.random() < self.mutationRate:
            geneToMutate = random.randint(0,self.numOfGenes-1)
            gene = copy.deepcopy(self.dictDir[self.listOfKeys[geneToMutate]])#copy cause we gonna modify
            gene.remove(individual.diretivas[self.listOfKeys[geneToMutate]]) #remove current gene value from the choices
            mutation = random.choice(gene)
            individual.diretivas[self.listOfKeys[geneToMutate]] = mutation
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
                offspringDirectives[key] = parent.diretivas[key]
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
        if self.dominateInBothMetrics(offspring,parent1,'resources','latency') and self.dominateInBothMetrics(offspring,parent2,'resources','latency'):
            #replace one of the parents randomly
            if random.random() < 0.5:
                parent1 = offspring
            else:
                parent2 = offspring
            return parent1,parent2
        #if offspring dominates parent1 in all objectives, replace parent1
        elif self.dominateInBothMetrics(offspring,parent1,'resources','latency'):
            parent1 = offspring
            return parent1,parent2
        #if offspring dominates parent2 in all objectives, replace parent2
        elif self.dominateInBothMetrics(offspring,parent2,'resources','latency'):
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
        return ((Solution2.resultados[metric1]>=Solution1.resultados[metric1]) or (Solution2.resultados[metric2] >= Solution1.resultados[metric2]))
        
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

    def __removeWorstSolution(self,topSolutions):
        worst = float('-inf')
        for solution in topSolutions:
            if solution.resultados['resources'] * solution.resultados['latency'] >= worst:
                worst = solution.resultados['resources'] * solution.resultados['latency']
                worstSolution = solution
        topSolutions.remove(worstSolution)