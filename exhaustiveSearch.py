from heuristic import Heuristic
import itertools
from pathlib import Path
from solution import Solution

class ExhaustiveSearch(Heuristic):

    def __init__(self,filePath,outPath):
        self.directivesTxt = Path(filePath).read_text()
        self.outPath = outPath
        self.solutions = self.createSolutionsLst()
    #Atributos dos caminhosdos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions
    


    def listOfDictsDirectives(self):
        dictDir = self.parsedTxt()                  
        keys, values = zip(*dictDir.items())
        permutations = [dict(zip(keys,v)) for v in itertools.product(*values)]
        #Gera uma lista de dicionários contendo todas as permutações possívels entre diretivas e valores 
        return permutations
    
    def createSolutionsLst(self):
        permutation = self.listOfDictsDirectives()
        solLst = []
        for diretivas in permutation:
            solution = Solution(diretivas)
            solution.runSynthesis()
            solLst.append(solution)
        #   Executa self.listOfDictsDirectives() e cria uma lista com as soluções geradas
        #a partir das diretivas
        return solLst

    def writeSolutions(self):
        output = ""
        data = self.solutions                   # O método toma a lista de soluções e imprime (em um arquivo)
        for element in data:                    #o dicionário de attrs
            diretivaResultado = str(element.__dict__)     #e.g{'diretivas': {'pipe': 'yes', ...}, 
            output += diretivaResultado                     # 'resultados': 8}
            output += "\n"
        Path(self.outPath).write_text(output)
 






