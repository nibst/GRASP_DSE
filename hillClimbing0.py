from importlib.metadata import PathDistribution, files
from re import S
from xml.dom.minidom import Element
from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy 

class HillClimbing(Heuristic):


    #A classe executa o a pseudo-heurística Hill-Climbing sobre as possíveis
    #   combinações de diretivas contidas no arquivo 'dFile' fornecido via terminal.
    #Um dicionário de soluções é criado.

    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        self.solutions = self.createSolutionsDict()
        


    def createSolutionsDict(self):
        
        dictDir=self.parsedTxt() 
        solutionsDict = {}
        final = dict.fromkeys(dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
            
        solutionIndex=0
        generateScript(self, self.directivesTxt,self.cFiles, self.prjFile)
        
        for diretiva in dictDir:  
            
            bestLUT = 999
            ##print(dictDir[diretiva])
            for option in dictDir[diretiva]:     
                
                if option == '':
                    option = None
                
                
                       
                final[diretiva] = option
                solution = Solution(final,self.cFiles,self.prjFile)    
                solution.runSynthesis()
                                                            #Progressivamente popula o dicionário 'final' e cria
                                                                #Solutions a partir deste
                
                
                if solution.resultados['LUT']<bestLUT:          #mantendo aquelas onde o nro de LUTs é estritamente
                    bestLUT = solution.resultados['LUT']        #menor que o da anterior.
                    
                    deep = copy.deepcopy(solution)   
                    solutionsDict[solutionIndex] = deep
                    solutionIndex+=1
                                        
                if solution.resultados['LUT']>bestLUT:
                    break

                                    # Retorna o dicionário de soluções para o 'main'
    
        return solutionsDict

    

    