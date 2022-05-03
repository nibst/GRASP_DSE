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
        
        final = dict.fromkeys(dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
        fileName = 'directives.tcl'                                 
            
        solutionIndex=1
        generateScript(self.cFiles, self.prjFile)
        
        keys,values = zip(*dictDir.items())
        permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
        index=1
        for element in permutations_dicts:
                #Progressivamente popula o dicionário 'final' e cria
            solution = Solution(element,self.cFiles,self.prjFile)         #Solutions a partir deste
            solution.runSynthesis()
       
            
            deep = copy.deepcopy(solution)   
            solutionsDict[solutionIndex] = deep               
            solutionIndex+=1

        return solutionsDict
 






