
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
from heuristics.heuristic import Heuristic
from pathlib import Path
from domain.solution import Solution
from utils.Script_tcl import generateScript
import copy
from random import seed
from random import randint
import random
from utils.abstractSolutionsSaver import SolutionsSaver

class RandomSearch(Heuristic):
    
    def __init__(self,filesDict,timeLimit=3600,solutionSaver:SolutionsSaver = None):
        super().__init__(filesDict)
        self.solutionSaver = solutionSaver
        self._SECONDS = timeLimit
        self.controlTree:dict = {}
        seed()
        self.run()

    def __generateRandomPermutation(self):
        node = self.controlTree
        newPermutation = {}
        directiveGroups = list(self.dictDir.keys()) 
        isNewPermutation = False #flag para verificar se é permutacao/solucao/design repetida ou nao
        for directive in directiveGroups:              
            domainLenght = len(self.dictDir[directive])   
            randomDirective = randint(0,domainLenght-1)
            newPermutation[directive] = self.dictDir[directive][randomDirective] 

            if self.isRestrictedDesign(newPermutation):
                break
            if randomDirective in node:
                node = node[randomDirective]
            else:
                node[randomDirective] = {} #cria nodo
                node = node[randomDirective]  
                isNewPermutation = True
        if isNewPermutation and not self.isRestrictedDesign(newPermutation):
            return newPermutation
        else:
            return None

    def run(self):
        onePermutation = {}
        generateScript(self.cFiles, self.prjFile)
        inTime = True
        start = time.time()
        while inTime:

            onePermutation = self.__generateRandomPermutation()
            if onePermutation:    #se tiver uma permutacao na variavel
                solution = Solution(onePermutation,self.cFiles,self.prjFile)         #Solutions a partir deste
                try:
                    synthesisTimeLimit = self._SECONDS - (time.time() - start) 
                    self.synthesisWrapper(solution,synthesisTimeLimit,self.solutionSaver)
                except Exception as e:
                    print(e)
                #executa else qnd try roda sem erros
                else:   
                    print(solution.results) 
                    print (len(self.solutions))      

            end = time.time()
            if self.solutionSaver:
                self.solutionSaver.save(self.solutions,'./time_stamps/timeStampRandomSearch')
            if end - start >= self._SECONDS: 
                break                
                        


    

    
