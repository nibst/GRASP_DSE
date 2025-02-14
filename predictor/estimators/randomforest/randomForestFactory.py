from predictor.estimators.estimatorFactory import EstimatorFactory
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
class RandomForestFactory(EstimatorFactory):
    def __init__(self,directivesFile):
        self.directivesFile = directivesFile
    def create(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        return RandomForestEstimator(self.directivesFile)