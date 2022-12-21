from predictor.estimators.estimatorFactory import EstimatorFactory
from predictor.estimators.m5p.m5pEstimator import M5PrimeEstimator
class M5PrimeFactory(EstimatorFactory):

    def __init__(self,directivesFile):
        self.directivesFile = directivesFile
    def create(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        return M5PrimeEstimator(self.directivesFile)