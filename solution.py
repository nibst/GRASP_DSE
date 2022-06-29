from random import randrange
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
import psutil

class Solution:
    _MAX_RAM_USAGE =50 #in percentage
    _DIRECTIVES_FILENAME = 'directives.tcl'
    _VIVADO_PROCESSNAME = 'vivado_hls'
    _FF_VALUE = 1; _LUT_VALUE = 2; _DSP_VALUE = 345.68; _BRAM_VALUE = 547.33

    
    def __init__(self,diretivas, cFile, prjFile):
        self.diretivas = diretivas
        self.cFile = cFile
        self.prjFile = prjFile
        resultados = {}
        resultados['FF'] = None
        resultados['DSP'] = None
        resultados['LUT'] = None
        resultados['BRAM'] = None
        resultados['resources'] = None
        resultados['latency'] = None
        self.resultados = resultados

    def setResultados(self,resultados:list):
        for index,key in enumerate(self.resultados):
            self.resultados[key] = resultados[index]
                
    def __writeDirectivesIntoFile(self):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in self.diretivas.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def runSynthesisTeste(self):
        resultados = {}
        resultados['FF'] = randrange(100)
        resultados['DSP'] = randrange(100)
        resultados['LUT'] = randrange(100)
        resultados['BRAM'] = randrange(100)
        resultados['resources'] = randrange(100)
        resultados['latency'] = randrange(100)

        self.resultados = resultados
   
    def runSynthesis(self):
        #TODO antes de chamar a sintese verificar se ja tem um processo do vivado rodando e fazer esse processo n ser confundido com o que vamos rodar
        #path to synthesis data
        xml='./Raise_dse/solution1/syn/report/csynth.xml'

        mydir='./Raise_dse'
        if os.path.exists(mydir):
            shutil.rmtree(mydir)
        self.__writeDirectivesIntoFile()
        print('Running Synthesis...')
        #vivado call using subprocess
        subprocess.Popen([r'./scriptBath.sh'])
        #testing if the synthesis ended
        vivadoIsRunning = True
                    
        time.sleep(2) #para dar tempo de iniciar vivado
        while vivadoIsRunning:
            #tempo entre duas checagens de se o vivado continua rodando
            time.sleep(1)
            vivadoIsRunning = False
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._VIVADO_PROCESSNAME:
                    vivadoIsRunning = True
                    memoryUse = proc.memory_percent()
                    if memoryUse > self._MAX_RAM_USAGE:
                        proc.terminate()
                        raise Exception("****Vivado_HLS has exceed max RAM usage****")
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
             raise Exception("****Error in synthesis****")       
