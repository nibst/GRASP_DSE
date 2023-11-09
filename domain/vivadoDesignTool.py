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
from exceptions.timeExceededException import TimeExceededException
class Vivado(DesignTool):
    
    
    def __init__(self, maxRAMUsage = 50, directivesFilename = './domain/directives.tcl'):
        self._MAX_RAM_USAGE = maxRAMUsage #in percentage
        self._DIRECTIVES_FILENAME = directivesFilename
        self._PROCESSNAME = 'vivado_hls'
        self._SCRIPT_PATH = './domain/callVivado.sh'
        self._FF_VALUE = 1; self._LUT_VALUE = 2; self._DSP_VALUE = 345.68; self._BRAM_VALUE = 547.33
        if sys.platform == 'win32':
            self._PROCESSNAME = 'vivado_hls.exe'
            self._SCRIPT_PATH = './domain/callVivado.bat'
        
    def runSynthesisTeste(self, solution: Solution, timeLimit=None, solutionSaver = None):
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
        solution.setresults(results)
        return solution
    
    def runSynthesis(self, solution: Solution, timeLimit = None, solutionSaver= None):
        self.__killOnGoingVivadoProcessIfAny()    
        #if not especified, there is infinite time to run synthesis
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception(f"****{self._PROCESSNAME} has exceed max time usage****")
        self.__writeDirectivesIntoFile(solution.directives)
        print('Running Synthesis...')
        #vivado call using subprocess
        subprocess.Popen([self._SCRIPT_PATH])
        self.__monitorVivadoProcess(timeLimit, solutionSaver)
        xml='./Raise_dse/solution1/syn/report/csynth.xml'
        results = self.__getResultsFromSynthesis(xml)
        for key in results:
            solution.setOneResult(key, results[key])
        return solution

    def __writeDirectivesIntoFile(self,directives):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in directives.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def __killOnGoingVivadoProcessIfAny(self):
        mydir='./Raise_dse'
        while os.path.exists(mydir):
            time.sleep(3)
            try:
                shutil.rmtree(mydir)
            except Exception as error:
                print(error)
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._PROCESSNAME:
                    proc.kill()
                    break        

    def __monitorVivadoProcess(self, timeLimit, solutionSaver):
        #testing if the synthesis ended
        vivadoIsRunning = True   
        start = time.time()
        while vivadoIsRunning:
            #time between checking if the process is still running
            time.sleep(3)
            vivadoIsRunning = False
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._PROCESSNAME:
                    vivadoIsRunning = True
                    #check memory usage
                    try:
                        memoryUse = proc.memory_percent()
                    except Exception as e:
                        print(e)
                        break
                    if memoryUse > self._MAX_RAM_USAGE:
                        proc.kill()   
                        raise Exception(f"****{self._PROCESSNAME} has exceed max RAM usage****")
                    #check time usage 
                    if time.time()-start >= timeLimit:
                        proc.kill()   
                        raise TimeExceededException(f"****{self._PROCESSNAME} has exceed max time usage****")
                    if solutionSaver:
                        solutionSaver.save(None,'./time_stamps/timeStampFiller')
                    break
        
    def __getResultsFromSynthesis(self, xmlPath:str):   
        results = {}
        if os.path.exists(xmlPath):  
            print("Synthesis ended")
            #read xml file
            tree = ET.parse(xmlPath)
            root = tree.getroot()

            x = root.find('AreaEstimates')
            x = x.find('Resources')
            results['FF'] =int(x.find('FF').text)
            results['DSP'] = int(x.find('DSP48E').text)
            results['LUT'] = int(x.find('LUT').text)
            results['BRAM'] = int(x.find('BRAM_18K').text)
            results['resources'] =  results['FF'] * self._FF_VALUE + results['LUT'] * self._LUT_VALUE + results['DSP'] * self._DSP_VALUE + results['BRAM'] * self._BRAM_VALUE    
            x = root.find('PerformanceEstimates')
            x = x.find('SummaryOfOverallLatency')
            try:
                results['latency'] = int(x.find('Average-caseLatency').text)
            except ValueError:
                raise ValueError("****UNDETERMINED LATENCY****")
        else:
            raise Exception("****Error in synthesis - NO Synthesis Results****")   
        return results    
