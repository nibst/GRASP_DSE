import copy
from random import randrange
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
import psutil
import sys
from exceptions.timeExceededException import TimeExceededException
class Solution:
    _MAX_RAM_USAGE =50 #in percentage
    _DIRECTIVES_FILENAME = './domain/directives.tcl'
    _VIVADO_PROCESSNAME = 'vivado_hls'
    _SCRIPT_PATH = './domain/callVivado.sh'
    _FF_VALUE = 1; _LUT_VALUE = 2; _DSP_VALUE = 345.68; _BRAM_VALUE = 547.33
    
    
    def __init__(self,directives:dict, cFile, prjFile):
        self.directives = copy.deepcopy(directives)
        self.cFile = cFile
        self.prjFile = prjFile
        if sys.platform == 'win32':
            self._VIVADO_PROCESSNAME = 'vivado_hls.exe'
            self._SCRIPT_PATH = './domain/callVivado.bat'
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
        for resultKey in self.results:
            if resultKey == key:
                self.results[key] = value
                break

    def setresults(self,results:list):
        for result in results:
            for index,key in enumerate(self.results):
                self.results[key] = result[index]
                
    def __writeDirectivesIntoFile(self):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in self.directives.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def runSynthesisTeste(self,timeLimit=None, solutionSaver = None):
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception("****Vivado_HLS has exceed max time usage****")
        results = {}
        results['FF'] = randrange(10)
        results['DSP'] = randrange(1)
        results['LUT'] = randrange(10)
        results['BRAM'] = randrange(2)
        results['resources'] = randrange(3)
        results['latency'] = randrange(4)

        self.results = results
   
    def runSynthesis(self,timeLimit = None, solutionSaver= None):
        #TODO antes de chamar a sintese verificar se ja tem um processo do vivado rodando e fazer esse processo n ser confundido com o que vamos rodar
        #path to synthesis data
        xml='./Raise_dse/solution1/syn/report/csynth.xml'
        mydir='./Raise_dse'
        while os.path.exists(mydir):
            time.sleep(3)
            try:
                shutil.rmtree(mydir)
            except Exception as error:
                print(error)
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._VIVADO_PROCESSNAME:
                    proc.kill()
                    break
            
        #if not especified, there is infinite time to run synthesis
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception("****Vivado_HLS has exceed max time usage****")

        self.__writeDirectivesIntoFile()
        print('Running Synthesis...')
        #vivado call using subprocess
        subprocess.Popen([self._SCRIPT_PATH])
        #testing if the synthesis ended
        vivadoIsRunning = True
                    
        start = time.time()
        
        while vivadoIsRunning:
            #tempo entre duas checagens de se o vivado continua rodando
            time.sleep(3)
            vivadoIsRunning = False
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._VIVADO_PROCESSNAME:
                    vivadoIsRunning = True
                    try:
                        memoryUse = proc.memory_percent()
                    except Exception as e:
                        print(e)
                        break
                    if memoryUse > self._MAX_RAM_USAGE:
                        proc.kill()   
                        raise Exception("****Vivado_HLS has exceed max RAM usage****")
                    
                    if time.time()-start >= timeLimit:
                        proc.kill()   
                        raise TimeExceededException("****Vivado_HLS has exceed max time usage****")
                    if solutionSaver:
                        solutionSaver.save(None,'./time_stamps/timeStampFiller')
                    break
            
        if os.path.exists(xml):  
            print("Synthesis ended")
            #TODO raise exception when passing a certain time constraint maybe
            #read xml file
            tree = ET.parse(xml)
            root = tree.getroot()

            results = {}
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
            self.results = results
        else:
             raise Exception("****Error in synthesis - NO Synthesis Results****")       
