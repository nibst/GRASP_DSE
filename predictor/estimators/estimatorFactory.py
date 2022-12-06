from abc import ABC,abstractmethod
class EstimatorFactory(ABC):
    """
    The Creator class declares the factory method that is supposed to return an
    object of a Product class. The Creator's subclasses usually provide the
    implementation of this method.
    """

    @abstractmethod
    def create(self,directivesFile):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass