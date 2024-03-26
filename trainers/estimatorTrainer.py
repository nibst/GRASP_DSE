import time
from heuristics.impl.RandomSearch import RandomSearch
from sklearn.model_selection import train_test_split


class RandomSamplesEstimatorTrainer:
    def __init__(self, filesDict, estimator, timeLimit,randomSampler=None):
        self._filesDict = filesDict
        self.estimator = estimator
        self._SECONDS = timeLimit
        self.score = -1
        self.timeSpent=0
    def trainUntilErrorThreshold(self, threshold,trainTimeBetweenThresholdsChecks):
        self.score = -1
        trainTime = trainTimeBetweenThresholdsChecks
        start = time.time()
        randomSearch = RandomSearch(self._filesDict,solutionSaver=None) 
        while self.score < threshold:
            remainingTime = self._SECONDS - (time.time() - self.start)
            if remainingTime <= self.TRAIN_TIME:
                trainTime = remainingTime
            else:
                trainTime = self.TRAIN_TIME
            randomSearch.run(trainTime)
            try:    
                train, test = train_test_split(randomSearch.solutions, test_size=0.2)
                self.estimator.trainModel(train)
                self.score = self.estimator.score(test)
            except Exception as e:
                self.score = -1 
                print(e)
            print(f'score: {self.score} ')
            #if time runs out
            if (time.time() - start) >= self._SECONDS:
                break
        self.estimator.trainModel(randomSearch.solutions) 
        self.timeSpent = time.time() -start
