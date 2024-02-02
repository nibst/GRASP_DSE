import argparse
import copy
import json
import pickle
from domain.solution import Solution
from predictor.estimators.estimatorFactory import EstimatorFactory
from predictor.estimators.randomforest import randomForest
from utils.Script_tcl import generateScript
from domain.designToolFactory import DesignToolFactory
from domain.desingTool import DesignTool

class CheckDirectivesImpact:
    def __init__(self, model, designTool:str = "vitis") -> None:
        self.designTool = DesignToolFactory.getDesignTool(designTool)
        self.solutions = []
        self.estimator = model  

    def getResults(self, possibleDirectives):
        appliedDirectives = dict.fromkeys(possibleDirectives,'')
        defaultSolution = Solution(appliedDirectives)
        estimatedResults = self.estimator.estimateSynthesis(defaultSolution)
        defaultSolution.setresults(estimatedResults)
        results = {}

        for directiveGroup in possibleDirectives:
            results[directiveGroup] = {}
            for directive in possibleDirectives[directiveGroup]:
                if directive != '':
                    appliedDirectives[directiveGroup] = directive
                    solution = Solution(appliedDirectives)
                    estimatedResults = self.estimator.estimateSynthesis(solution)
                    solution.setresults(estimatedResults)
                    self.solutions.append(solution)
                    latencyGainPercentage = 1 - (solution.results['latency']/defaultSolution.results['latency'])
                    resourcesGainPercentage = 1 -(solution.results['resources']/defaultSolution.results['resources'])
                    results[directiveGroup][directive] = {'latency': latencyGainPercentage, 'resources': resourcesGainPercentage}              

                appliedDirectives[directiveGroup] = ''    
        return results
                                 
    def writeResultsToFile(self, results, outputFilename):
        with open(outputFilename, 'w') as f:
            json.dump(results,f)
        

