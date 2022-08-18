import time
from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy
from random import randint,seed


class GA(Heuristic):
    def __init__(self,filesDict,outPath,numOfGenerations = 10):
        super().__init__(filesDict, outPath)
        self.dictDir =self.parsedTxt()
        self.numOfIndividuals = len(self.dictDir.keys()) 
        self.numOfGenerations = numOfGenerations
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
        listOfKeys = list(self.dictDir.keys()) #to use numbers (indexes of list) instead of strings in the algorithm logic
        population = self.randomSample() #list of random Solutions (without their HLS results yet)
        for i in range(self.numOfGenerations):
            new_population = []
            while len(new_population) < self.numOfIndividuals:
                parent1,parent2 = self.selector(population)
                offspring1,offspring2 = self.crossover(parent1,parent2)
                offspring1 = self.mutation(offspring1)
                offspring2 = self.mutation(offspring2)
                new_population.extend([offspring1,offspring2])
        population = new_population
        return self.top(2,population)


    def selector(self,population,numOfIndividuals):
        #tournament
        part = self.__uniformRandom(population,numOfIndividuals)
        return self.top(2,part)

    def __uniformRandom(self,population,numOfIndividuals):
        domainLenght = len(population)
        indexes = [] # indexes of the individuals that got selected
        i = 0
        while i < numOfIndividuals:
            individualIndex = randint(0,domainLenght-1)
            if individualIndex not in indexes:
                indexes.append()
                i+=1
        part = [] #list of the population that gonna be returned
        for index in indexes:
            part.append(population[index])
        return part
            
    def randomSample(self,randomState = 1):
        controlTree = {}
        sample = []
        seed(randomState)
        onePermutation = None
        i=0
        while i<(self.numOfIndividuals):
            onePermutation = self.__generateRandomPermutation(controlTree)
            if onePermutation:
                solution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste
                sample.append(solution)
                i+=1
        return sample

    def top(self,numOfTops, population:list[Solution]):

        topSolutions = [] #top "numOfTops" solutions
        for count,individual in enumerate(population):
            try:
                self.synthesisWrapper(individual)
            except Exception as e:
                print(e)
            else:
                if count >= numOfTops:
                    self.__removeWorstSolution(topSolutions)
                topSolutions.append(individual) 
        return topSolutions

    def mutation():
        pass

    def __generateRandomPermutation(self,controlTree:dict):
        node = controlTree
        newPermutation = {}
        isNewPermutation = False #flag para verificar se é permutacao/solucao/design repetida ou nao
        for directive in self.dictDir:              
            domainLenght = len(self.dictDir[directive])   
            randomDirective = randint(0,domainLenght-1)
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