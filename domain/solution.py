import copy
import json
import os
from pathlib import Path
from typing import List, Tuple, Union
from exceptions.timeExceededException import TimeExceededException
import xml.etree.ElementTree as ET

class Solution:
    
    def __init__(self,directives:dict = None, period = 8):
        self.period = period #in nano seconds
        if directives:
            self.directives = copy.deepcopy(directives)
            if directives.get('period',None):
                self.period = directives['period']
                self.directives.pop('period')

        else: 
            self.directives = {}
        self.solution_name = "solution"
        results = {}
        results['FF'] = None
        results['DSP'] = None
        results['LUT'] = None
        results['BRAM'] = None
        results['resources'] = None
        results['latency'] = None
        self.results = results
        self.FF_VALUE = 1; self.LUT_VALUE = 2; self.DSP_VALUE = 345.68; self.BRAM_VALUE = 547.33

    def set_directives(self,directives:dict):
        """
        set directives used in this solution
        """
        self.directives = copy.deepcopy(directives)

    def set_one_result(self,key,value):
        self.results[key] = value

    def set_results(self,results:dict):
        self.results = results.copy() #ensure that we are not modifying the original results
    
    def set_results_with_results_list(self, results:list):
        for result in results:
            for index,key in enumerate(self.results):
                self.results[key] = result[index]
    
    def set_period(self,period):
        self.period = period

    def has_valid_results(self):
        """
        Validate the results of the synthesis. 
        Check if the results are valid and not None.
        """
        for key in self.results:
            if self.results[key] is None:
                return False, Exception(f"****{key} is None****")
            if self.results[key] < 0:
                return False, Exception(f"****{key} is negative****")
        return True, None