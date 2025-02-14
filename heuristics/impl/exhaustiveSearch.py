from heuristics.heuristic import Heuristic
from pathlib import Path
from domain.solution import Solution
from utils.Script_tcl import generateScript
import copy
import itertools
import time
class ExhaustiveSearch(Heuristic):
    _SECONDS = 2
    def __init__(self,filesDict):
        super().__init__(filesDict)

        self.run()
        
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions



    def run(self):        
        keys,values = zip(*self.dictDir.items())
        totalTime = 0
        count =0
        start = time.time()
        invalid= 0
        print(f'total:{self.countAllSpace()}')
        print(f'with function: {self.countPrunnedSpace()}')
        for permutation in itertools.product(*values):
            start = time.time()
            perumtationDict = dict(zip(keys,permutation)) # one permutation
            
            solution = Solution(perumtationDict)         #Solutions a partir deste
            if not self.isRedundantDesign(solution.directives):
                count+=1
            else:
                invalid+=1
    
            try:
                #chama synthesis e salva em self.solutions
                self.synthesisWrapper(solution)
            except Exception as e:
                print(e)
            
            end = time.time()
            totalTime += (end-start)
            if totalTime >= self._SECONDS: #time that this will run for
                return 
        print(count)
        print(invalid)
        
        
       
 






