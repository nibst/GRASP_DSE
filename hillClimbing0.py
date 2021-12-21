from heuristic import Heuristic
from pathlib import Path
from solution import Solution

class HillClimbing(Heuristic):
    def __init__(self,filePath,outPath):
        self.directivesTxt = Path(filePath).read_text()
        self.outPath = outPath
        self.solutions = self.createSolutionsLst()
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions

    def createSolutionsLst(self):
        dictDir=self.parsedTxt() 
        currentBest = {}
        for diretiva in dictDir:       #Percorre o dict de diretivas procurando o melhor valor             
            best = 0                            #ali presente e assim segue até encontrar um menor 
            for valor in dictDir[diretiva]:     #que o atual melhor. Isto quebra o laço e passa para
                solution = Solution(currentBest)    #a próxima diretiva.
                solution.runSynthesis()
                if solution.resultados>best:
                    best = solution.resultados
                    currentBest[diretiva] = valor
                    break
                
        
        return currentBest

    