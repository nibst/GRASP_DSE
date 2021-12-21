from heuristic import Heuristic
from pathlib import Path
from solution import Solution

class Greedy(Heuristic):
    def __init__(self,filePath,outPath):
        self.directivesTxt = Path(filePath).read_text()
        self.outPath = outPath
        self.solutions = self.createSolutionsLst()
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions

    def createSolutionsLst(self):
        dictDir=self.parsedTxt() 
        currentBest = {}
        for diretiva in dictDir:                        #Percorre o dict de diretivas procurando o melhor valor
            best = 0                                    # em cada uma destas
            for valor in dictDir[diretiva]:
                solution = Solution(currentBest)        #As soluções são iniciadas com os atuais melhores  
                solution.runSynthesis()                     # valores encontrados ate o momento 
                if solution.resultados>best:                  # e atualiza sse um melhor
                    best = solution.resultados
                    currentBest[diretiva] = valor
                
        
        return currentBest
