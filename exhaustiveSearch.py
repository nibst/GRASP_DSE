from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy
import itertools
import time
class ExhaustiveSearch(Heuristic):
    _SECONDS = 48800
    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        self.solutions = self.createSolutionsDict()
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions



    def createSolutionsDict(self):
        
        solutionsDict = {}
                    
        
        solutionIndex=1
        generateScript(self.cFiles, self.prjFile)
        
        keys,values = zip(*self.dictDir.items())
        totalTime = 0
        for permutation in itertools.product(*values):
            start = time.time()
            perumtationDict = dict(zip(keys,permutation)) # one permutation
            
            solution = Solution(perumtationDict,self.cFiles,self.prjFile)         #Solutions a partir deste
            try:
                solution.runSynthesis()
            except Exception as e:
                print(e)
            else:
                print(solution.resultados)             
                deep = copy.deepcopy(solution)   
                solutionsDict[solutionIndex] = deep
                print (solutionIndex)               
                solutionIndex+=1
            end = time.time()
            totalTime += (end-start)
            if totalTime >= self._SECONDS: #time that this will run for
                return solutionsDict
        return solutionsDict
        
       
 






