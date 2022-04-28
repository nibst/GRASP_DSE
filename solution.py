from random import randrange
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
class Solution:

    def __init__(self,diretivas, cFile, prjFile):
        self.diretivas = diretivas
        self.cFile = cFile
        self.prjFile = prjFile

    def runSynthesisTeste(self):
        resultados = {}
        resultados['LUT'] = randrange(100)
        resultados['FF'] = randrange(100)
        resultados['DSP'] = randrange(100)
        resultados['BRAM'] = randrange(100)
        resultados['latency'] = randrange(100)

        self.resultados = resultados
   
    def runSynthesis(self):
        #path to synthesis data
        xml='./Raise_dse/solution1/syn/report/csynth.xml'
        
        mydir='./Raise_dse'
        if os.path.exists(xml):
            shutil.rmtree(mydir)

        print('Running Synthesis...')
        #vivado call using subprocess
        subprocess.call([r'scriptBath.bat'])
        #testing if the synthesis ended
        while not os.path.exists(xml):
            time.sleep(1)
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
            print("WARNING: UNDETERMINED LATENCY")
            resultados['latency'] = -1

        self.resultados = resultados        
