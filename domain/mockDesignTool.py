from random import randrange
from domain.designTool import DesignTool
from domain.solution import Solution
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
import psutil
import sys
from exceptions.timeExceededException import TimeExceededException
class MockDesignTool(DesignTool):
    
    def __init__(self, maxRAMUsage = 50, directivesFilename = './domain/directives.tcl'):
        pass
        
    def runSynthesis(self, solution,cFiles,prjFile, timeLimit=None, solutionSaver=None, run_implementation=True):
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception(f"****{self._PROCESSNAME} has exceed max time usage****")
        results = {}
        results['FF'] = randrange(10)
        results['DSP'] = randrange(1)
        results['LUT'] = randrange(10)
        results['BRAM'] = randrange(2)
        results['resources'] = randrange(3)
        results['latency'] = randrange(4)
        solution.set_results(results)
        return solution
    
      
