import copy
from exceptions.timeExceededException import TimeExceededException
class Solution:
    
    def __init__(self,directives:dict):
        self.directives = copy.deepcopy(directives)
        results = {}
        results['FF'] = None
        results['DSP'] = None
        results['LUT'] = None
        results['BRAM'] = None
        results['resources'] = None
        results['latency'] = None
        self.results = results

    def setDirectives(self,directives:dict):
        """
        set directives used in this solution
        """
        self.directives = copy.deepcopy(directives)

    def setOneResult(self,key,value):
        self.results[key] = value

    def setresults(self,results:list):
        for result in results:
            for index,key in enumerate(self.results):
                self.results[key] = result[index]
                   
