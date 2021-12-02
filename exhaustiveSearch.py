from heuristic import Heuristic
import itertools

from solution import Solution

class ExhaustiveSearch(Heuristic):

    

    def listOfDictsDirectives(self):
        dictDir = self.parsedTxt()
        keys, values = zip(*dictDir.items())
        permutation = [dict(zip(keys,v)) for v in itertools.product(*values)]
        return permutation
    
    def createSolutions(self,permutation):
        for diretivas in permutation:
            solution = Solution(diretivas)
            solution.runSynthesis()
            print(diretivas)
            print(solution.resultados)
            
            
            




h0 = ExhaustiveSearch('directivesFile.txt')
permutation = h0.listOfDictsDirectives()
h0.createSolutions(permutation)

