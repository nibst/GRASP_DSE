from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy
import itertools

class ExhaustiveSearch(Heuristic):

    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        self.solutions = self.createSolutionsDict()
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions



    def createSolutionsDict(self):
        
        dictDir=self.parsedTxt() 
        solutionsDict = {}
        
        
        fileName = 'directives.tcl'                                 
            
        
        solutionIndex=1
        generateScript(self.cFiles, self.prjFile)
        
        keys,values = zip(*dictDir.items())
        permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
        
        for element in permutations_dicts:
                #Progressivamente popula o dicionário 'final' e cria
            solution = Solution(element,self.cFiles,self.prjFile)         #Solutions a partir deste
            solution.runSynthesis()
            directivesFile = open(fileName, "w")
            for value in solution.diretivas.values():
                if value is not None:
                    directivesFile.write(value + '\n')
                print(value)
            directivesFile.close()
       
            
            deep = copy.deepcopy(solution)   
            solutionsDict[solutionIndex] = deep
            print (solutionIndex)               
            solutionIndex+=1

        return solutionsDict
 






