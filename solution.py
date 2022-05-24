from random import randrange
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
import psutil

class Solution:
    _MAX_RAM_USAGE = 30 #in percentage
    _DIRECTIVES_FILENAME = 'directives.tcl'
    _VIVADO_PROCESSNAME = 'vivado_hls.exe'
    def __init__(self,diretivas, cFile, prjFile):
        self.diretivas = diretivas
        self.cFile = cFile
        self.prjFile = prjFile
        
    def __writeDirectivesIntoFile(self):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in self.diretivas.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def runSynthesisTeste(self):
        resultados = {}
        resultados['LUT'] = randrange(100)
        resultados['FF'] = randrange(100)
        resultados['DSP'] = randrange(100)
        resultados['BRAM'] = randrange(100)
        resultados['latency'] = randrange(100)

        self.resultados = resultados
   
    def runSynthesis(self):
        #TODO antes de chamar a sintese verificar se ja tem um processo do vivado rodando e fazer esse processo n ser confundido com o que vamos rodar
        #path to synthesis data
        xml='./Raise_dse/solution1/syn/report/csynth.xml'
        
        mydir='./Raise_dse'
        if os.path.exists(xml):
            shutil.rmtree(mydir)
        self.__writeDirectivesIntoFile()
        print('Running Synthesis...')
        #vivado call using subprocess
        subprocess.Popen([r'scriptBath.bat'])
        
        #testing if the synthesis ended
        vivadoIsRunning = True
        while vivadoIsRunning:
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
        x = root.find('PerformanceEstimates')
        x = x.find('SummaryOfOverallLatency')
        try:
            resultados['latency'] = int(x.find('Average-caseLatency').text)
        except ValueError:
            raise ValueError("****UNDETERMINED LATENCY****")
        self.resultados = resultados        
