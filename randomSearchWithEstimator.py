import time
from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy
from random import seed
from random import randint
from RandomSearch import RandomSearch
from greedy import Greedy
from randomForest import RandomForestEstimator


class RandomSearchWithEstimator(Heuristic):
    _SECONDS = 1600 
    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        sample = RandomSearch(filesDict, outPath)
        #sample2 = Greedy(filesDict,outPath,'resources')
        self.rf = RandomForestEstimator(filesDict['dFile'])
        self.rf.trainModel(sample.solutions)
        #self.rf.trainModel(sample2.solutions)
        self.solutions = self.createSolutionsDict()
        
    def __generateRandomPermutation(self,dictDir:dict,controlTree:dict):
        node = controlTree
        newPermutation = {}
        isNewPermutation = False #flag para verificar se é permutacao/solucao/design repetida ou nao
        for directive in dictDir:              
            domainLenght = len(dictDir[directive])   
            randomDirective = randint(0,domainLenght-1)
            newPermutation[directive] = dictDir[directive][randomDirective] 
            if randomDirective in node:
                node = node[randomDirective]
            else:
                node[randomDirective] = {} #cria nodo
                node = node[randomDirective]
                isNewPermutation = True
        if isNewPermutation:
            return newPermutation
        else:
            return self.__generateRandomPermutation(dictDir,controlTree)

    def __estimateTopSolutions(self,dictDir,controlTree):
        estimatedSolutions = []
        topSolutions = [] #top 10 solutions
        for i in range(1000):
            onePermutation = self.__generateRandomPermutation(dictDir,controlTree)
            if onePermutation:
                estimatedSolution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste     
                estimatedResults = self.rf.estimateSynthesis(estimatedSolution)
                estimatedSolution.setResultados(estimatedResults[0])
                estimatedSolutions.append(estimatedSolution)
                print(f'estimated solution: {estimatedSolution.resultados}')
                if i >= 10:
                    self.__removeWorstSolution(topSolutions)
                topSolutions.append(estimatedSolution)
        return topSolutions
                    
    def __removeWorstSolution(self,topSolutions):
        worst = float('-inf')
        for solution in topSolutions:
            if solution.resultados['resources'] >= worst:
                worst = solution.resultados['resources']
                worstSolution = solution
        topSolutions.remove(worstSolution)

    def createSolutionsDict(self):
        dictDir=self.parsedTxt() 
        solutionsDict = {}
        onePermutation = {}
        controlTree = {}
        
        solutionIndex=0
        generateScript(self.cFiles, self.prjFile)
        inTime = True
        seed(1)
        totalTime = 0
        while inTime:
            start = time.time()
            topEstimatedSolutions = self.__estimateTopSolutions(dictDir,controlTree)
            print(topEstimatedSolutions)
            topSynthesized = [] #synthesis of the top estimated solutions
            for estimatedSolution in topEstimatedSolutions:    
                solution = Solution(estimatedSolution.diretivas,self.cFiles,self.prjFile)         #Solutions a partir deste
                try:
                    solution.runSynthesis()
                except Exception as e:
                    print(e)
                #executa else qnd try roda sem erros
                else:   
                    print(solution.resultados)                  
                    deep = copy.deepcopy(solution)   
                    solutionsDict[solutionIndex] = deep
                    topSynthesized.append(deep)
                    print (solutionIndex)      
                    solutionIndex+=1
            #retrain
            self.rf.trainModel(topSynthesized)
            end = time.time()
            totalTime += (end-start)
            if totalTime >= self._SECONDS: 
                return solutionsDict                            
                    

                                        # Retorna o dicionário de soluções para o 'main'
        print(f'score: {self.rf.score(solutionsDict)}')
        return solutionsDict
