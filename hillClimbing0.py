from importlib.metadata import files
from re import S
from xml.dom.minidom import Element
from heuristic import Heuristic
from pathlib import Path
from solution import Solution
import copy 

class HillClimbing(Heuristic):
    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFile = filesDict['cFile']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        self.solutions = self.createSolutionsDict()
        
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions
        

    def createSolutionsDict(self):
        pass
        dictDir=self.parsedTxt() 
        
        solutionLst = []
        currentBest = {}
        solutionsDict = {}
        solutionIndex=0
        for diretiva in dictDir:  

            best = 0

            #print("###"+diretiva)     #Percorre o dict de diretivas procurando o melhor valor             
            
            for option in dictDir[diretiva]:     #que o atual melhor. Isto quebra o laço e passa para
            
                currentBest[diretiva] = option
                solution = Solution(currentBest,self.cFile,self.prjFile)    #a próxima diretiva.
                solution.runSynthesis()
                
                
                if solution.resultados['LUT']>best:
                    best = solution.resultados['LUT']
                    #print("Best: "+option)
                    #print(best)
                    
                    currentBest[diretiva] = option
                    
                    deep = copy.deepcopy(solution.diretivas)   #shallow copia os dados em cada ireração
                    
                    solutionsDict[solutionIndex] = deep
                    solutionIndex+=1
                                        
                if solution.resultados['LUT']<best:
                    break
        
        return solutionsDict

    

    