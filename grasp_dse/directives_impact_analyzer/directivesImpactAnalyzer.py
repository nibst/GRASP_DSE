from abc import ABC, abstractmethod
import json

class DirectivesImpactAnalyzer(ABC):
    def __init__() -> None:
        pass

    @abstractmethod
    def getImpacts(self, possibleDirectives):
        pass
    
    def setImpacts(self, impacts):
        self.impacts = impacts

    def writeImpactsToFile(self, outputFilename):
        with open(outputFilename, 'w') as f:
            json.dump(self.impacts,f)
        

