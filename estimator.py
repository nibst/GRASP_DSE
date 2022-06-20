from abc import ABC, abstractmethod
from solution import Solution
class Estimator(ABC):

    def __init__(self,dataset):
        self.dataset = dataset #lista de objetos da Solution (solucoes de um design) já sintetizados. Para treino/teste     
        self.features = self._extractFeatures() #pega tudo menos o 'Y' (que seria o queremos estimar)
        self.results = self._extractResults() #pega o 'Y'

    @abstractmethod
    def estimateSynthesis(self,solution:Solution): #solution é um objeto da Solution não sintetizado. Para inferencia
        pass
    
    #TODO talvez n precise ter esse, remover esse futuramente provavelmente
    @abstractmethod
    def trainModel(self):
        pass


    def _extractFeatures1(self):
        features = [] #lista de listas
        for solution in self.dataset:
            thisSolutionDirectives =[]
            for diretiva in solution.diretivas:
                thisSolutionDirectives.append(solution.diretivas[diretiva])
            features.append(thisSolutionDirectives)
        #print(features)
        return features

    def _extractFeatures(self):
        features = [] #lista de listas
        for solutionIndex in range(len(self.dataset)):
            thisSolutionDirectives =[]
            for diretiva in self.dataset[solutionIndex].diretivas:
                thisSolutionDirectives.append(self.dataset[solutionIndex].diretivas[diretiva])
            features.append(thisSolutionDirectives)
        #print(features)
        return features
        
    def _extractResults(self):
        results = []
        for solutionIndex in range(len(self.dataset)):
            solutionResults = []
            for metric in self.dataset[solutionIndex].resultados:
                solutionResults.append(self.dataset[solutionIndex].resultados[metric])
            results.append(solutionResults)
        #print(results)
        return results
        
    def _extractResults1(self):
        results = []
        for solution in self.dataset:
            results.append(solution.resultados)
        #print(results)
        return results
    
    def _takeColumns(self):
        columnsDict = {}
        featuresTypes = self.dataset[0].diretivas

        for directiveType in featuresTypes:
            featuresColumn = []
            for solution in self.dataset:
                featuresColumn.append(self.dataset[solution].diretivas[directiveType])
            columnsDict[directiveType] = featuresColumn
        return columnsDict

   
        