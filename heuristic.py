from pathlib import Path
import readDirectivesFile
from solution import Solution

class Heuristic:

    def __init__(self,filePath,outPath):
        self.directivesTxt = Path(filePath).read_text()
        self.outPath = outPath
        
    def parsedTxt(self):
        return readDirectivesFile.fileParser(self.directivesTxt)

    def writeSolutions(self,data):
        output = ""
        for element in data:
            diretivaResultado = str(element.__dict__)
            output += diretivaResultado
            output += "\n"
        Path(self.outPath).write_text(output)



    
    


