from abc import ABC, abstractmethod
from importlib.resources import path
import readDirectivesFile
from pathlib import Path
import os,glob

class Heuristic(ABC):


    def parsedTxt(self):
        return readDirectivesFile.fileParser(self.directivesTxt)
    #Passa para o arquivo readDirectivesFile.py o texto lido do arquivo

    

    @abstractmethod                         # Método abstrato a sere herdados e implementado
    def createSolutionsDict(self):           # pelas classes filhas
        pass

    def writeSolutionsDict(self):
        outputGeral = ""    
                             #Percorre a lista de diretivas da solução escolhida
        data = self.solutions               #   pela heurística e o imprime usando a biblio Path

        
        for element in data:
            outputSolution = ""
            #print("########## \n#Solução de Índice " + str(element) + "\n------------")
            outputGeral+="########## \n#Solucao de indice " + str(element) + "\n##########\n"
            outputSolution+="########## \n#Solucao de indice " + str(element) + "\n##########\n"
            for diretiva in data[element]:
                outputGeral+= diretiva + ':' + data[element][diretiva] +'\n'
                outputSolution+= diretiva + ':' + data[element][diretiva] +'\n'
            
            pathFolder = 'directivesBySolution'
            files = glob.glob(pathFolder)
            for file in files:
                os.remove(file)
            solDirPath =pathFolder+'/' + str(element) + '.tcl'
            
            try: os.mkdir(pathFolder)
            except:pass
            Path(solDirPath).write_text(outputSolution)
        outPathGeneral='directivesGroupBySolution.tcl'
        Path(outPathGeneral).write_text(outputGeral)


        
            
        
    
    

    




    
    


