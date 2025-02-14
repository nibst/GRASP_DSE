
from domain.designToolFactory import DesignToolFactory
from domain.solution import Solution
from directives_impact_analyzer.directivesImpactAnalyzer import DirectivesImpactAnalyzer


class SynthesisBasedDirectivesImpactAnalyzer(DirectivesImpactAnalyzer):
    def __init__(self, designTool = 'vitis') -> None:
        self.impacts = None
        self.designTool = DesignToolFactory.getDesignTool(designTool)


    def getImpacts(self, possibleDirectives):
        if self.impacts is not None:
            #just get the impacts that are from possible directives

            impacts = dict(filter(lambda item: item[0] in possibleDirectives, self.impacts.items()))
            return impacts
        
        appliedDirectives = dict.fromkeys(possibleDirectives,'')
        defaultSolution = Solution(appliedDirectives)
        #if default solution runs into exception, then theres nothing we can do
        try:
            solution = self.designTool.runSynthesis(defaultSolution)
        except Exception as e:
            raise
        impacts = {}
        for directiveGroup in possibleDirectives:
            impacts[directiveGroup] = {}
            for directive in possibleDirectives[directiveGroup]:
                if directive != '':
                    appliedDirectives[directiveGroup] = directive
                    solution = Solution(appliedDirectives)
                    try:
                        solution = self.designTool.runSynthesis(solution)
                    except Exception as e:
                        impacts[directiveGroup][directive] = {'latency': -0.00001, 'resources': -0.00001}#just to be a little worse than no gain, we set as -0.00001
                        print(e)
                    else:
                        latencyGainPercentage = 1 - (solution.results['latency']/defaultSolution.results['latency'])
                        resourcesGainPercentage = 1 -(solution.results['resources']/defaultSolution.results['resources'])
                        impacts[directiveGroup][directive] = {'latency': latencyGainPercentage, 'resources': resourcesGainPercentage}              

                appliedDirectives[directiveGroup] = ''   
        self.impacts = impacts 
        return impacts
                                 

