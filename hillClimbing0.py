from importlib.metadata import PathDistribution, files
from re import S
from xml.dom.minidom import Element
from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from solutionTimeXLUT import SolutionTimeXLUT
from Script_tcl import generateScript

from datetime import timedelta

import copy


class HillClimbing(Heuristic):


    #A classe executa o a pseudo-heurística Hill-Climbing sobre as possíveis
    #   combinações de diretivas contidas no arquivo 'dFile' fornecido via terminal.
    #Um dicionário de soluções é criado.

    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        self.solutions = self.createSolutionsDict()
        

    def createSolutionsDict(self):
        dictDir=self.parsedTxt() 
        solutionsDict = {}
        txlDict = {}
        final = dict.fromkeys(dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
        
        solutionIndex=0
        generateScript(self.cFiles, self.prjFile)
        
        for diretiva in dictDir:  
            
            bestLUTxLatency = float('inf') #infinito
            ##print(dictDir[diretiva])
            for option in dictDir[diretiva]:     
                
                if option == '':
                    option = None
                       
                final[diretiva] = option                             #Progressivamente popula o dicionário 'final' e cria
                solution = Solution(final,self.cFiles,self.prjFile)         #Solutions a partir deste
                try:
                    solution.runSynthesis()
                except Exception as e:
                    final[diretiva] = None #retira a diretiva usada
                    print(e)
                #executa else qnd try roda sem erros
                else:   
                    print(solution.resultados)              
                    lutXLatency = solution.resultados['LUT'] * solution.resultados['latency']
                    if lutXLatency<bestLUTxLatency:          #mantendo aquelas onde o nro de LUTs é estritamente
                        bestLUTxLatency = lutXLatency        #menor que o da anterior.
                        
                        deep = copy.deepcopy(solution)   
                        solutionsDict[solutionIndex] = deep
                        solutionIndex+=1
                                            
                    if lutXLatency>bestLUTxLatency:
                        break

                                    # Retorna o dicionário de soluções para o 'main'
    
        return solutionsDict


    

    