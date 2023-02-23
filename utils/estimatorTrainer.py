

import time
from heuristics.impl.RandomSearch import RandomSearch
from sklearn.model_selection import train_test_split


class RandomSamplesEstimatorTrainer:
    def __init__(self, filesDict, estimator, timeLimit,randomSampler=None):
        self._filesDict = filesDict
        self.estimator = estimator
        self._SECONDS = timeLimit
        self.score = -1
    def trainUntilErrorThreshold(self, threshold,trainTimeBetweenThresholdsChecks):
        score = -1
        valueToLowerThreshold = 0.05
        trainTime = trainTimeBetweenThresholdsChecks
        start = time.time()
        sample = RandomSearch(self._filesDict,trainTime,solutionSaver=None)
        while score < threshold:
            try:    
                train, test = train_test_split(sample.solutions, test_size=0.2)
                self.estimator.trainModel(train)
                
                score = self.estimator.score(test)
            except Exception as e:
                #do nothing, just train more
                score = -1 
                print(e)            
            print(f'score: {score} ')

            if score < threshold: 
                #create more samples
                sample.run()

            #if the time spent creating a new model is x times the trainTime, lower the threshold
            if time.time() - start >= trainTime*3:
                threshold -= valueToLowerThreshold

            #if time runs out
            if (time.time() - start) >= self._SECONDS:
                break
        self.score = score
        self.estimator.trainModel(sample.solutions) 

