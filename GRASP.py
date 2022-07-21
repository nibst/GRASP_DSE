from heuristic import Heuristic
from pathlib import Path
from solution import Solution
from Script_tcl import generateScript
import copy
import random



class GRASP(Heuristic):
    
    
    
    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        self.solutions = self.createSolutionsDict()
       
    
    def createSolutionsDict(self):
        
        dictDir=self.parsedTxt() 
        diretivas = dict.fromkeys(dictDir,'') #Cria um dicionário 'diretivas' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                            #trocados por None
        solutionIndex=0
        solutionsDict = {}
        generateScript(self.cFiles, self.prjFile)

        num_iter = 3
        i = 1
        while i <= num_iter:
            P = Solution(diretivas,self.cFiles,self.prjFile)            ##### Design 0        
            P.runSynthesisTeste()
            
            vizinhosP = self.vizinhosP(P,dictDir,diretivas)             #
            RCL = self.paretoSolutions('LUT','latency',vizinhosP)      # Construção do RCL filtrando vizinhos
            P = self.biased(RCL)                                        # Biased Random
            
            deep = copy.deepcopy(P)   
            solutionsDict[solutionIndex] = deep               
            solutionIndex+=1    

            vizinhosP = self.vizinhosP(P,dictDir,diretivas)
            melhor = self.melhor(vizinhosP)

            deep = copy.deepcopy(P)   
            solutionsDict[solutionIndex] = deep               
            solutionIndex+=1
            print(i)
            i+=1

        return solutionsDict

    def vizinhosP(self,P,dictDir,diretivas):
        vizinhos = {}
        solutionIndex = 0
        for dir in P.diretivas:
            for newDir in dictDir[dir]:
               if newDir != P.diretivas[dir]:
                    deep = copy.deepcopy(diretivas)                 
                    
                    newVizinho = deep
                    newVizinho[dir] = newDir
                    vizinho = Solution(newVizinho,self.cFiles,self.prjFile)
                    vizinho.runSynthesisTeste()
                    deep = copy.deepcopy(vizinho)   
                    vizinhos[solutionIndex] = deep               
                    solutionIndex+=1
        return vizinhos

    def biased(self,RCL):
        somaLXL = 0
        listLxL = []                    #### Está escolhendo o de maior LutXLat, preciso ainda ver como
        listaParetos = []               #### distribuir os pesos para escolher o de menor
        for element in RCL:
            lut = RCL[element].resultados['LUT']
            lat = RCL[element].resultados['latency']
            
            lutXlat = lut*lat
            
            listLxL.append(lutXlat*10)
            listaParetos.append(RCL[element])
            somaLXL += lutXlat
        
        tupleLxL = tuple(listLxL)        
        P = random.choices(listaParetos, weights=tupleLxL)[0]
        

        return(P)
    
    def melhor(self,vizinhosP):
        menorlxl = 99999999999
        melhor = 0
        for element in vizinhosP:
            metrica = vizinhosP[element].resultados['LUT'] * vizinhosP[element].resultados['latency'] 
            if metrica < menorlxl:
                menorlxl = metrica
                melhor = element
        return vizinhosP[melhor]

