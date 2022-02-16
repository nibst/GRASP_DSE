from random import randrange
import os
class Solution:

    def __init__(self,diretivas, cFile, prjFile):
        self.diretivas = diretivas
        self.cFile = cFile
        self.prjFile = prjFile

    
    def runSynthesis(self):

        resultados = {}
        resultados['LUT'] = randrange(100)
        resultados['FF'] = randrange(100)
        resultados['DSP'] = randrange(100)
        resultados['BRAM'] = randrange(100)
        resultados['latency'] = randrange(100)

        self.resultados = resultados
   
