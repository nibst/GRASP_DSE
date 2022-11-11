from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy

class Greedy(Heuristic):
    
    
    
    def __init__(self,filesDict,outPath,metricName):
        super().__init__(filesDict, outPath)
        self.metric = metricName

        #Gera soluções conforme métodos abaixo e as salva num dict em self.solutions
        self.createSolutionsDict()

    def createSolutionsDict(self):
        
        
        final = dict.fromkeys(self.dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
        generateScript(self.cFiles, self.prjFile)

        for diretiva in self.dictDir: 
            currentBest = None
            bestMetricxLatency = float('inf') #infinito
            
            for option in self.dictDir[diretiva]:   
                
                if option == '':
                    option = None

                final[diretiva] = option                             #Progressivamente popula o dicionário 'final' e cria
                solution = Solution(final,self.cFiles,self.prjFile)         #Solutions a partir deste     
                try:
                    #chama synthesis e salva em self.solutions
                    self.synthesisWrapper(solution)
                except Exception as e:
                    final[diretiva] = None #retira a diretiva usada
                    print(e)
                #executa else qnd try roda sem erros    
                else:
                    print(solution.resultados)             
                    metricXLatency = solution.resultados[self.metric] * solution.resultados['latency']
                    if metricXLatency<bestMetricxLatency:          #mantendo aquelas onde o nro de LUTs é estritamente
                        bestMetricxLatency = metricXLatency
                        currentBest = option        #menor que o da anterior.              
            final[diretiva] = currentBest
                                        