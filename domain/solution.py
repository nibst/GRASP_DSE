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
    _MAX_RAM_USAGE =30 #in percentage
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
        resultados = {}
        resultados['FF'] = None
        resultados['DSP'] = None
        resultados['LUT'] = None
        resultados['BRAM'] = None
        resultados['resources'] = None
        resultados['latency'] = None
        self.resultados = resultados

    def setDirectives(self,directives:dict):
        """
        set directives used in this solution
        """
        self.directives = copy.deepcopy(directives)

    def setOneResult(self,key,value):
        for resultKey in self.resultados:
            if resultKey == key:
                self.resultados[key] = value
                break

    def setResultados(self,results:list):
        for result in results:
            for index,key in enumerate(self.resultados):
                self.resultados[key] = result[index]
                
    def __writeDirectivesIntoFile(self):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in self.directives.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def runSynthesisTeste(self,timeLimit=None):
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception("****Vivado_HLS has exceed max time usage****")
        resultados = {}
        resultados['FF'] = randrange(100)
        resultados['DSP'] = randrange(100)
        resultados['LUT'] = randrange(100)
        resultados['BRAM'] = randrange(100)
        resultados['resources'] = randrange(100)
        resultados['latency'] = randrange(100)

        self.resultados = resultados
   
    def runSynthesis(self,timeLimit = None):
        #TODO antes de chamar a sintese verificar se ja tem um processo do vivado rodando e fazer esse processo n ser confundido com o que vamos rodar
        #path to synthesis data
        xml='./Raise_dse/solution1/syn/report/csynth.xml'

        #if not especified, there is infinite time to run synthesis
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception("****Vivado_HLS has exceed max time usage****")
            
        mydir='./Raise_dse'
        if os.path.exists(mydir):
            try:
                shutil.rmtree(mydir)
            except Exception as error:
                for proc in psutil.process_iter(['name']):
                    if proc.name() == self._VIVADO_PROCESSNAME:
                        proc.kill()
                        break
                shutil.rmtree(mydir)
        self.__writeDirectivesIntoFile()
        print('Running Synthesis...')
        #vivado call using subprocess
        subprocess.Popen([self._SCRIPT_PATH])
        #testing if the synthesis ended
        vivadoIsRunning = True
                    
        time.sleep(2) #para dar tempo de iniciar vivado
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
                        #proc.terminate()
                        print(e)
                        break
                    if memoryUse > self._MAX_RAM_USAGE:
                        proc.kill()   
                        raise Exception("****Vivado_HLS has exceed max RAM usage****")
                    
                    if time.time()-start >= timeLimit:
                        proc.kill()   
                        raise TimeExceededException("****Vivado_HLS has exceed max time usage****")
                    break
            
        if os.path.exists(xml):  
            print("Synthesis ended")
            #TODO raise exception when passing a certain time constraint maybe
            #read xml file
            tree = ET.parse(xml)
            root = tree.getroot()

            resultados = {}
            x = root.find('AreaEstimates')
            x = x.find('Resources')
            resultados['FF'] =int(x.find('FF').text)
            resultados['DSP'] = int(x.find('DSP48E').text)
            resultados['LUT'] = int(x.find('LUT').text)
            resultados['BRAM'] = int(x.find('BRAM_18K').text)
            resultados['resources'] =  resultados['FF'] * self._FF_VALUE + resultados['LUT'] * self._LUT_VALUE + resultados['DSP'] * self._DSP_VALUE + resultados['BRAM'] * self._BRAM_VALUE    
            x = root.find('PerformanceEstimates')
            x = x.find('SummaryOfOverallLatency')
            try:
                resultados['latency'] = int(x.find('Average-caseLatency').text)
            except ValueError:
                raise ValueError("****UNDETERMINED LATENCY****")
            self.resultados = resultados
        else:
             raise Exception("****Error in synthesis - NO Synthesis Results****")       