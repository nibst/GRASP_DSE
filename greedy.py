from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy

class Greedy(Heuristic):
    
    
    
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
        solutionIndex=1
        generateScript(self.cFiles, self.prjFile)
        
        for diretiva in dictDir: 

            
            
            
            bestLUTxLatency = float('inf') #infinito
            
            for option in dictDir[diretiva]:   
                
                
                if option == '':
                    option = None
                 
                
                       
                final[diretiva] = option                             #Progressivamente popula o dicionário 'final' e cria
                solution = Solution(final,self.cFiles,self.prjFile)         #Solutions a partir deste
                solution.runSynthesis()
                print(solution.resultados)             
                lutXLatency = solution.resultados['LUT'] * solution.resultados['latency']
                if lutXLatency<bestLUTxLatency:          #mantendo aquelas onde o nro de LUTs é estritamente
                    bestLUTxLatency = solution.resultados['LUT']
                    currentBest = option        #menor que o da anterior.
                    
                deep = copy.deepcopy(solution)   
                solutionsDict[solutionIndex] = deep               
                solutionIndex+=1
            final[diretiva] = currentBest
                                        
            # Retorna o dicionário de soluções para o 'main'
        
        return solutionsDict