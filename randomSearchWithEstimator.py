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
    
    """
    Random search with estimator:

    Use an estimator to get the top "_NUM_OF_TOP" designs
    out of the "_NUM_OF_ESTIMATED" random estimated designs. The top desings get synthesized 
    and are added to the dict that will be returned.
    The top designs are used to retrain the model (after them beign synthesized)
    
    Attributes
    ----------
    _SECONDS : int
        number of seconds that the function ``createSolutionsDict`` runs for
    
    _NUM_OF_TOP : int
        number of estimated designs that will be select to be on the top designs list
        that will be synthesized 
    _NUM_OF_ESTIMATED : int
        number of designs that will explored by estimating in that iteration
    """

    _SECONDS = 3600
    _NUM_OF_TOP = 10
    _NUM_OF_ESTIMATED = 1000
    def __init__(self,filesDict,outPath):#TODO receber como parametro de modelo preditivo
        
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        sample = RandomSearch(filesDict, outPath)
        sample2 = Greedy(filesDict,outPath,'resources')
        for solutionIndex in sample.solutions.keys():
            pass
        for solution in sample2.solutions.values():
            solutionIndex+=1
            sample.solutions[solutionIndex] = solution
        self.sample = sample
        
        self.rf = RandomForestEstimator(filesDict['dFile'])
        self.rf.trainModel(sample.solutions)
        self.solutions = self.createSolutionsDict()
        """
        for solutionIndex in self.solutions.keys():
            pass
        for solution in sample.solutions.values():
            solutionIndex+=1
            self.solutions[solutionIndex] = solution
        """
        
    def __initializeControlTree(self,dictDir:dict,controlTree:dict):
        #colocar as sinteses do sample aqui pra n rodar novamente
        
        for solution in self.sample.solutions.values():
            node = controlTree
            for directiveType in solution.diretivas.keys():
                directive=solution.diretivas[directiveType]
                if directive == None:
                    directive = ''
                #a control tree representa cada diretiva como numero, na ordem do dictDir, ent pegar o numero
                directiveIndex = dictDir[directiveType].index(directive) 
                if directiveIndex in node:
                    node = node[directiveIndex]
                else:
                    node[directiveIndex] = {} #cria nodo
                    node = node[directiveIndex]

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
            return None

    def __estimateTopSolutions(self,dictDir,controlTree):
        estimatedSolutions = []
        topSolutions = [] #top 10 solutions
        count = 0
        for i in range(self._NUM_OF_ESTIMATED):
            onePermutation = self.__generateRandomPermutation(dictDir,controlTree)
            if onePermutation:
                estimatedSolution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste     
                estimatedResults = self.rf.estimateSynthesis(estimatedSolution)
                estimatedSolution.setResultados(estimatedResults[0])
                estimatedSolutions.append(estimatedSolution)
                #print(f'estimated solution: {estimatedSolution.resultados}')
                if i >= self._NUM_OF_TOP:
                    self.__removeWorstSolution(topSolutions)
                topSolutions.append(estimatedSolution)
            else: count+=1
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
        controlTree = {}
        self.__initializeControlTree(dictDir,controlTree)
        solutionIndex=0
        generateScript(self.cFiles, self.prjFile)
        inTime = True
        seed(2)
        totalTime = 0
        start = time.time()
        while inTime:
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
                end = time.time()
                totalTime = (end-start)
                if totalTime >= self._SECONDS:
                    return solutionsDict 
                
            #retrain
            print(f'score: {self.rf.score(topSynthesized)}')
            self.rf.trainModel(topSynthesized)
                                      
        
                                        # Retorna o dicionário de soluções para o 'main'
        return solutionsDict
