from heuristic import Heuristic
from pathlib import Path
from solution import Solution

class BestOfEach(Heuristic):
    def __init__(self,filePath,outPath):
        self.directivesTxt = Path(filePath).read_text()
        self.outPath = outPath
        self.solutions = self.createSolutionsLst()
    #Atributos dos caminhosdos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions

    def createSolutionsLst(self):
        dictDir=self.parsedTxt() 
        currentBest = {}
        
        for diretiva in dictDir:
            min = 0
            for valor in dictDir[diretiva]:
                solution = Solution(currentBest)
                solution.runSynthesis()
                if solution.resultados>min:
                    min = solution.resultados
                    currentBest[diretiva] = valor
                    
        print(currentBest.values())

        return dictDir

    def writeSolutions(self):
        return super().writeSolutions()