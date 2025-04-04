from random import randrange
from domain.desingTool import DesignTool
from domain.solution import Solution
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
import psutil
import sys
from domain.solution_factory import SolutionFactory
from exceptions.timeExceededException import TimeExceededException
from utils import parser
from utils.Script_tcl import generate_script_for_implementation, generateScript

class Vitis(DesignTool):
    
    def __init__(self, maxRAMUsage = 95, directivesFilename = './domain/directives.tcl'):
        self._MAX_RAM_USAGE = maxRAMUsage #in percentage
        self._DIRECTIVES_FILENAME = directivesFilename
        self._PROCESSNAME = 'vitis_hls'
        self._IMPL_PROCESSNAME = 'vivado'
        self._SCRIPT_PATH = './domain/callVitis.sh'
        if sys.platform == 'win32':
            self._PROCESSNAME = 'vitis_hls.exe'
            self._SCRIPT_PATH = './domain/callVitis.bat'
        
    def runSynthesis(self, solution: Solution, c_files, top_func, timeLimit = None, solutionSaver= None, run_implementation=False):
        self.__killOnGoingVitisProcessIfAny()    
        #if not especified, there is infinite time to run synthesis
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception(f"****{self._PROCESSNAME} has exceed max time usage****")
        self.__writeDirectivesIntoFile(solution.directives)
        if run_implementation:
            generate_script_for_implementation(c_files,top_func,solution.period)
        else:
            generateScript(c_files,top_func,solution.period)
        print('Running Synthesis...')
        #vitis call using subprocess
        subprocess.Popen([self._SCRIPT_PATH])
        self.__monitorVitisProcess(timeLimit, solutionSaver)

        vitis_solution_path = './Raise_dse/solution1/'
        if run_implementation:
            resources_utilization = parser.extract_impl_utilization(vitis_solution_path, filtered=False) 
        else:
            resources_utilization = parser.extract_hls_utilization(vitis_solution_path,filtered=False)
        latency = parser.extract_hls_cc_report(vitis_solution_path, filtered=False)
        results = resources_utilization | {"latency" : latency}
        results["resources"] = parser.compute_snru(results, vitis_solution_path, filtered=False)
        solution.set_results(results)
        are_valid_results, error = solution.has_valid_results()
        if not are_valid_results:
            raise error

        print (results)
        return solution

    def __writeDirectivesIntoFile(self,directives):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in directives.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def __killOnGoingVitisProcessIfAny(self):
        mydir='./Raise_dse'
        while os.path.exists(mydir):
            time.sleep(3)
            try:
                shutil.rmtree(mydir)
            except Exception as error:
                print(error)
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._PROCESSNAME or proc.name() == self._IMPL_PROCESSNAME:
                    proc.kill()
                    break        

    def __monitorVitisProcess(self, timeLimit, solutionSaver):
        #testing if the synthesis ended
        vitisIsRunning = True   
        start = time.time()
        while vitisIsRunning:
            #time between checking if the process is still running
            time.sleep(3)
            vitisIsRunning = False
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._PROCESSNAME or proc.name() == self._IMPL_PROCESSNAME:
                    vitisIsRunning = True
                    #check memory usage
                    try:
                        memoryUse = proc.memory_percent()
                    except Exception as e:
                        print(e)
                        break
                    if proc.name() == self._IMPL_PROCESSNAME:
                        ninety_percent = 90
                        if memoryUse > ninety_percent:
                            proc.kill()   
                            raise Exception(f"****{self._IMPL_PROCESSNAME} has exceed max RAM usage****")
                    elif memoryUse > self._MAX_RAM_USAGE:
                        proc.kill()   
                        raise Exception(f"****{self._PROCESSNAME} has exceed max RAM usage****")
                    #check time usage 
                    if time.time()-start >= timeLimit:
                        proc.kill()   
                        raise TimeExceededException(f"****{self._PROCESSNAME} has exceed max time usage****")
                    if solutionSaver:
                        solutionSaver.save(None,'./time_stamps/timeStampFiller')
                    break

