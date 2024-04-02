from abc import ABC
import argparse
import copy
import json
import pickle
from domain.solution import Solution
from predictor.estimators.estimatorFactory import EstimatorFactory
from predictor.estimators.randomforest import randomForest
from directives_impact_analyzer.directivesImpactAnalyzer import DirectivesImpactAnalyzer


class EstimatorBasedDirectivesImpactAnalyzer(DirectivesImpactAnalyzer):
    def __init__(self, model) -> None:
        self.impacts = None
        self.estimator = model  

    def getImpacts(self, possibleDirectives):
        if self.impacts is not None:
            return self.impacts
        
        appliedDirectives = dict.fromkeys(possibleDirectives,'')
        defaultSolution = Solution(appliedDirectives)
        estimatedResults = self.estimator.estimateSynthesis(defaultSolution)
        defaultSolution.setResultsWithListOfResults(estimatedResults)
        impacts = {}

        for directiveGroup in possibleDirectives:
            impacts[directiveGroup] = {}
            for directive in possibleDirectives[directiveGroup]:
                if directive != '':
                    appliedDirectives[directiveGroup] = directive
                    solution = Solution(appliedDirectives)
                    estimatedResults = self.estimator.estimateSynthesis(solution)
                    solution.setResultsWithListOfResults(estimatedResults)
                    latencyGainPercentage = 1 - (solution.results['latency']/defaultSolution.results['latency'])
                    resourcesGainPercentage = 1 -(solution.results['resources']/defaultSolution.results['resources'])
                    impacts[directiveGroup][directive] = {'latency': latencyGainPercentage, 'resources': resourcesGainPercentage}              

                appliedDirectives[directiveGroup] = ''   
        self.impacts = impacts 
        return impacts
                                 

        
