from abc import ABC, abstractmethod
from importlib.resources import path
import readDirectivesFile
from pathlib import Path

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
             #   print (diretiva, ':', data[element][diretiva])
            solDirPath = str(element) + '.txt'
            Path(solDirPath).write_text(outputSolution)
        Path(self.outPath).write_text(outputGeral)
            
        pass
            
        
    
    def writeSolutionsTcl(self):
        output = ""                         #Percorre a lista de dirpetivas da solução escolhida
        data = self.solutions               #   pela heurística e o imprime usando a biblio Path
        
        for element in data:
            diretivaResultado = data[element]
            if diretivaResultado != '':
                output += diretivaResultado + "\n"
        

        Path(self.outPath).write_text(output)

    




    
    


