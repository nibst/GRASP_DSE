
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
        seed()
        self.run()
    def setTimeLimit(self,seconds):
        self._SECONDS = seconds
    def run(self):
        onePermutation = {}
        inTime = True
        start = time.time()
        controlTree:dict = {}
        while inTime:

            onePermutation = self.generateRandomPermutation(controlTree)
            if onePermutation:    #se tiver uma permutacao na variavel
                solution = Solution(onePermutation)         #Solutions a partir deste
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
                        


    

    
