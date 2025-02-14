from random import randrange
from predictor.estimators.estimator import Estimator
from domain.solution import Solution
class RandomEstimator(Estimator):
        
    def trainModel(self):
        pass 
    def estimateSynthesis(self,solution:Solution):
        results= {}
        results['LUT'] = randrange(100)
        results['FF'] = randrange(100)
        results['DSP'] = randrange(100)
        results['BRAM'] = randrange(100)
        results['latency'] = randrange(100)
        solution.results = results
        return solution

    def isTrained(self):
        return True