from heuristics.heuristic import Heuristic
from pathlib import Path
from domain.solution import Solution
from utils.Script_tcl import generateScript
import copy

class Greedy(Heuristic):
    
    
    
    def __init__(self,filesDict,metricName):
        super().__init__(filesDict)
        self.metric = metricName
        self.run()

    def run(self):
        final = dict.fromkeys(self.dictDir,None)
        """
        generate tcl script that uses input IR for synthesis
        for each operation:
            option = get the option (v2c or no v2c) that gets the min fitness
            select this option

            
        """ 
        for diretiva in self.dictDir: 
            currentBest = None
            bestMetricxLatency = float('inf') #infinito
            
            for option in self.dictDir[diretiva]:   
                if option == '':
                    option = None

                final[diretiva] = option           #Progressivamente popula o dicionário 'final' e cria
                solution = Solution(final)         #Solutions a partir deste     
                try:
                    #chama synthesis e salva em self.solutions
                    self.synthesisWrapper(solution)
                except Exception as e:
                    final[diretiva] = None #retira a diretiva usada
                    print(e)
                #executa else qnd try roda sem erros    
                else:
                    print(solution.results)             
                    metricXLatency = solution.results[self.metric] * solution.results['latency']
                    if metricXLatency<bestMetricxLatency:          #mantendo aquelas onde o nro de LUTs é estritamente
                        bestMetricxLatency = metricXLatency
                        currentBest = option        #menor que o da anterior.              
            final[diretiva] = currentBest

    def _fitness(self,mseValue,resourcesXLatency):
        if mseValue == 0:
            return resourcesXLatency
        else:
            return resourcesXLatency / mseValue 