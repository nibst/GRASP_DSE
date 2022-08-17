from sklearn.base import RegressorMixin 
from estimator import Estimator
import re
from preProcessor import PreProcessor
from solution import Solution
from pathlib import Path
import readDirectivesFile
from m5py import M5Prime
import numpy as np
class M5PrimeEstimator(Estimator):
    
    def __init__(self,directivesFile):
        self.m5prime = M5Prime()
        self.features = []
        self.results = []
        self.processor = PreProcessor(directivesFile)

    def trainModel(self,dataset):
        """
        Build a forest of trees from the dataset.
        Can be retrained with with new data
        Parameters
        ----------
        dataset : List of Solution objects
        """
        features, results = self.processor.process(dataset)
        self.features.extend(features)
        self.results.extend(results)
        features = np.array(self.features) 
        results = np.array(self.results)
        try:
            self.m5prime.fit(features,results) #train
        except Exception as e:
            print("ERROR: M5P doesnt work predicting for multiple outputs")
            raise e
    def trainModelPerMetric(self,dataset:dict,metric):
        features, results = self.processor.process(dataset)
        results = []
        for solution in dataset.values():
            results.append(solution.resultados[metric])
        self.features.extend(features)
        self.results.extend(results)
        features = np.array(self.features) 
        results = np.array(self.results)
        
        self.m5prime.fit(features,results) #train

    def estimateSynthesis(self, dataset):
        #TODO talvez futuramente retornar lista de solutions
        """
        Estimate the output of synthesis from the dataset.

        Parameters
        ----------
        dataset: List of Solution objects

        Returns
        -------
        List : List of the output([FF,DSP,LUT,BRAM,resources,latency],[...],...)
                estimated for these features
        """
        processedFeatures, processedResults =  self.processor.process(dataset)
        return self.m5prime.predict(processedFeatures)

    
    def score(self,dataset):
        processedFeatures, processedResults =  self.processor.process(dataset)
        return self.m5prime.score(self.m5prime,processedFeatures,processedResults)

