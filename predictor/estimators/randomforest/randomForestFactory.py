from predictor.estimators.estimatorFactory import EstimatorFactory
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
class RandomForestFactory(EstimatorFactory):

    def create(self,directivesFile):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        return RandomForestEstimator(directivesFile)