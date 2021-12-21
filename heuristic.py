from abc import ABC, abstractmethod
import readDirectivesFile
from pathlib import Path

class Heuristic(ABC):


    def parsedTxt(self):
        return readDirectivesFile.fileParser(self.directivesTxt)
    #Passa para o arquivo readDirectivesFile.py o texto lido do arquivo

    

    @abstractmethod                         # Método abstrato a sere herdados e implementado
    def createSolutionsLst(self):           # pelas classes filhas
        pass

    def writeSolutions(self):
        output = ""                         #Percorre a lista de diretivas da solução escolhida
        data = self.solutions               #   pela heurística e o imprime usando a biblio Path

        for element in data:
            diretivaResultado = data[element]
            output += '{'+element+' : '
            output += diretivaResultado + '}'
            output += "\n"
            
        print(output)
        Path(self.outPath).write_text(output)
      
    



    
    


