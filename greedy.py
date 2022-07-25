from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy

class Greedy(Heuristic):
    
    
    
    def __init__(self,filesDict,outPath,metricName):
        super().__init__(filesDict, outPath)
        self.metric = metricName
        self.solutions = self.createSolutionsDict()
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions

    
    def createSolutionsDict(self):
        
        dictDir=self.parsedTxt() 
        solutionsDict = {}
        
        final = dict.fromkeys(dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
        solutionIndex=0
        generateScript(self.cFiles, self.prjFile)

        for diretiva in dictDir: 
            currentBest = None
            bestMetricxLatency = float('inf') #infinito
            
            for option in dictDir[diretiva]:   
                
                
                if option == '':
                    option = None

                final[diretiva] = option                             #Progressivamente popula o dicionário 'final' e cria
                solution = Solution(final,self.cFiles,self.prjFile)         #Solutions a partir deste     
                try:
                    self.synthesisWrapper(solution,solutionsDict)
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
                                        
            # Retorna o dicionário de soluções para o 'main'
        return solutionsDict
