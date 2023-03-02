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
        self.score = -1
        trainTime = trainTimeBetweenThresholdsChecks
        start = time.time()
        sample = RandomSearch(self._filesDict, self._outPath,trainTime,solutionSaver=None) 
        while self.score < threshold:
            try:    
                train, test = train_test_split(sample.solutions, test_size=0.2)
                self.estimator.trainModel(train)
                self.score = self.estimator.score(test)
            except Exception as e:
                #do nothing, just train more
                self.score = -1 
                print(e)
            print(f'score: {self.score} ')
            #if time runs out
            if (time.time() - start) >= self._SECONDS:
                break
            if self.score < threshold: 
                #create more samples
                sample.run()
        self.score = score
        self.estimator.trainModel(sample.solutions) 
