import time
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
        #como o m5prime não aceita modelo preditivo para múltiplos outputs precisa de um modelo para cada output
        self.latencyModel = M5Prime()
        self.LUTModel = M5Prime()
        self.BRAMModel = M5Prime()
        self.DSPModel = M5Prime()
        self.FFModel = M5Prime()
        self.resourcesModel= M5Prime()
        self.features = []
        self.results = []
        self.processor = PreProcessor(directivesFile)

    def trainModel(self,dataset):
        """
        Build m5p from the dataset.
        Parameters
        ----------
        dataset : List of Solution objects
        """
        try:
            start = time.time()
            self.__trainModelPerMetric(dataset,"latency",self.latencyModel)
            self.__trainModelPerMetric(dataset,"LUT",self.LUTModel)
            self.__trainModelPerMetric(dataset,"BRAM",self.BRAMModel)
            self.__trainModelPerMetric(dataset,"DSP",self.DSPModel)
            self.__trainModelPerMetric(dataset,"FF",self.FFModel)
            self.__trainModelPerMetric(dataset,"resources",self.resourcesModel)
            #print(time.time() - start)
        except Exception as e:
            print(e)
            raise e
    def __trainModelPerMetric(self,dataset:dict,metric,model:M5Prime):
        features, results = self.processor.process(dataset)
        results = []
        for i in range(len(dataset)): # works for both dict and list of solutions that are serial keys
            results.append(dataset[i].resultados[metric])
        
        features = np.array(features) 
        results = np.array(results)

        model.fit(features,results) #train

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
        latency = self.latencyModel.predict(processedFeatures)
        LUT = self.LUTModel.predict(processedFeatures)
        BRAM = self.BRAMModel.predict(processedFeatures)
        DSP = self.DSPModel.predict(processedFeatures)
        FF = self.FFModel.predict(processedFeatures)
        resources = self.resourcesModel.predict(processedFeatures)
        results=np.array([FF,DSP,LUT,BRAM,resources,latency])
        results = np.transpose(results)
        return results

    def __scorePerMetric(self,dataset,metric,model:M5Prime):
        features, results =  self.processor.process(dataset)
        results = []
        for i in range(len(dataset)): # works for both dict and list of solutions that are serial keys
            results.append(dataset[i].resultados[metric])
        return model.score(features,results)
     
    def score(self,dataset):
        """
        median score of all the models 
        """
        latencyScore = self.__scorePerMetric(dataset,"latency",self.latencyModel)
        LUTScore = self.__scorePerMetric(dataset,"LUT",self.LUTModel)
        BRAMScore =self. __scorePerMetric(dataset,"BRAM",self.BRAMModel)
        DSPScore = self.__scorePerMetric(dataset,"DSP",self.DSPModel)
        FFScore = self.__scorePerMetric(dataset,"FF",self.FFModel)
        resourcesScore = self.__scorePerMetric(dataset,"resources",self.resourcesModel)
        return (latencyScore+LUTScore+BRAMScore+DSPScore+FFScore+resourcesScore)/6
    #TODO
    def cross_validation_score(self,dataset):
        pass    
