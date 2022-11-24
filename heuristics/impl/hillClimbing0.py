from heuristics.heuristic import Heuristic
from domain.solution import Solution
from utils.Script_tcl import generateScript

import copy


class HillClimbing(Heuristic):


    #A classe executa o a pseudo-heurística Hill-Climbing sobre as possíveis
    #   combinações de diretivas contidas no arquivo 'dFile' fornecido via terminal.
    #Um dicionário de soluções é criado.

    def __init__(self,filesDict,outPath):
        super().__init__(filesDict, outPath)    
        self.createSolutionsDict()
    def createSolutionsDict(self):
        
        solutionsDict = {}
        txlDict = {}
        final = dict.fromkeys(self.dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
        
        solutionIndex=0
        generateScript(self.cFiles, self.prjFile)
        
        for diretiva in self.dictDir:  
            
            bestResourcesxLatency = float('inf') #infinito
            ##print(dictDir[diretiva])
            for option in self.dictDir[diretiva]:     
                
                if option == '':
                    option = None
                       
                final[diretiva] = option                             #Progressivamente popula o dicionário 'final' e cria
                solution = Solution(final,self.cFiles,self.prjFile)         #Solutions a partir deste
                try:
                    self.synthesisWrapper(solution)
                except Exception as e:
                    final[diretiva] = None #retira a diretiva usada
                    print(e)
                #executa else qnd try roda sem erros
                else:   
                    print(solution.resultados)              
                    resourcesXLatency = solution.resultados['resources'] * solution.resultados['latency']
                    if resourcesXLatency<bestResourcesxLatency:          #mantendo aquelas onde o nro de LUTs é estritamente
                        bestResourcesxLatency = resourcesXLatency        #menor que o da anterior.
                                            
                    else:
                        break

    

    