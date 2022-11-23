from random import randrange
from predictor.estimators.estimator import Estimator
from domain.solution import Solution
class RandomEstimator(Estimator):
        
    def trainModel(self):
        pass 
    def estimateSynthesis(self,solution:Solution):
        resultados= {}
        resultados['LUT'] = randrange(100)
        resultados['FF'] = randrange(100)
        resultados['DSP'] = randrange(100)
        resultados['BRAM'] = randrange(100)
        resultados['latency'] = randrange(100)
        solution.resultados = resultados
        return solution
    