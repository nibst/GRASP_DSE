from pathlib import Path
import readDirectivesFile


class Heuristic:

    def __init__(self,filePath):
        self.directivesTxt = Path(filePath).read_text()
        
    def parsedTxt(self):
        return readDirectivesFile.fileParser(self.directivesTxt)
    

