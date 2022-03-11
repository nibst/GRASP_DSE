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

    # def writeDirectivesFile(self,directive,path):
    #     output = ""
    #     for element in directive:
    #         output += element
    #         output+= '\n'
    #         output+=directive[element]
    #         output+= '\n'
    #     Path(path).write_text(output)

    def writeSolutionsDict(self):
        outputGeral = ""    
                             
        data = self.solutions               
                
        for solutionNmbr in data:
            outputSolution = ""
        #     outputGeral+="########## \n#Solucao de indice " + str(element) + "\n##########\n"
            outputSolution+="########## \n#Solucao de indice " + str(solutionNmbr) + "\n##########\n"
            #print(solutionNmbr)
            #print(data[solutionNmbr].diretivas)
            for diretiva in data[solutionNmbr].diretivas:
                #print(diretiva)
                #print(data[solutionNmbr].diretivas[diretiva])
        #         outputGeral+= diretiva + ':' + data[element][diretiva] +'\n'
                outputSolution+= diretiva + ' : ' + str(data[solutionNmbr].diretivas[diretiva]) +'\n'
            print (outputSolution)
            
        #     pathFolder = 'directivesBySolution'
            
        #     solDirPath =pathFolder+'/' + str(element) + '.tcl'
            
        #     try: os.mkdir(pathFolder)
        #     except:pass
        #     Path(solDirPath).write_text(outputSolution)
        # outPathGeneral='directivesGroupBySolution.tcl'
        # Path(outPathGeneral).write_text(outputGeral)

    