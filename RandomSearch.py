
#---------------------------------------------------------------------------------------------------------------------------------------
#Cada tipo de diretiva sera chamado de uma "variavel".
#Pra fazer o random, para cada variavel será randomizado um valor de seu dominio. 
#Exemplo: Variavel de "unroll main", pode ter como dominio: None, set_directive_unroll -factor 4, set_directive_unroll -factor 8.
#         Portanto nesse caso diremos que essa variavel pode assumir os valores 0,1,2 . 0 sempre será a opção de None (sem aquela diretiva)

#arvore de controle para checar se permutacao ja foi vista
#EXEMPLO: primeiro tipo de diretiva:       [0 | 1 ]
#                                         / | \    \  
#         segundo tipo de diretiva:     [0 |1 |2]  [1]
#E vai indo, os numeros representam qual diretiva foi usada das possiveis diretivas daquele tipo. "0" representa None (sem aquela diretiva)
#---------------------------------------------------------------------------------------------------------------------------------------
import json
import time
from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy
from random import seed
from random import randint


class RandomSearch(Heuristic):
    
    def __init__(self,filesDict,outPath,timeLimit=3600):
        super().__init__(filesDict, outPath)
        self._SECONDS = timeLimit
        self.controlTree:dict = {}
        self.createSolutionsDict()
        seed(1)

    def __generateRandomPermutation(self,dictDir:dict):
        node = self.controlTree
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

    def createSolutionsDict(self):
        onePermutation = {}
        generateScript(self.cFiles, self.prjFile)
        inTime = True
        totalTime = 0
        while inTime:
            start = time.time()
            
            onePermutation = self.__generateRandomPermutation(self.dictDir)
            if onePermutation:    #se tiver uma permutacao na variavel
                solution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste
                try:
                    synthesisTimeLimit = self._SECONDS - (time.time() - start) 
                    self.synthesisWrapper(solution,synthesisTimeLimit)
                except Exception as e:
                    print(e)
                #executa else qnd try roda sem erros
                else:   
                    print(solution.resultados)                  
                    print (self.solutionIndex)      

            end = time.time()
            totalTime += (end-start)
            if totalTime >= self._SECONDS: 
                break                
                        


    

    
