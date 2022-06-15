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

    def __compareSolutions(self,Solution1,Solution2,metric1,metric2):
        #testa se a Solution1  domina a Solution2
        return ((Solution2.resultados[metric1]>Solution1.resultados[metric1]) and (Solution2.resultados[metric2] > Solution1.resultados[metric2]))
    def paretoSolutions(self,metric1,metric2 ):
        """consegue as soluções que são dominadas por outras. Eliminas essas soluções, retorando só nas que são pareto
            Retorna um dicionário enumerado de paretos(soluções). Ex: paretos[0],paretos[1],etc. paretos[i] == algum objeto Solution"""
        toRemove = [] #armazena o indice da solução que deve ser eliminada
        paretoCandidates = [] #armazena indice das solucoes candidatas a pareto, é inicializada com todos indices
        solutionsIndex = []
        #inicializa
        for i in range(len(self.solutions)):
            paretoCandidates.append(i)
            solutionsIndex.append(i)
            
        for currentSolutionIndex in solutionsIndex:
            if currentSolutionIndex in paretoCandidates:
                for paretoSolutionIndex in paretoCandidates:
                    if currentSolutionIndex != paretoSolutionIndex:
                        #se current solution dominar a solucao candidate a pareto
                        if(self.__compareSolutions(self.solutions[currentSolutionIndex],self.solutions[paretoSolutionIndex],metric1,metric2)):
                            toRemove.append(paretoSolutionIndex)
                        #se a solucao candidata a pareto dominar a current solution
                        elif(self.__compareSolutions(self.solutions[paretoSolutionIndex],self.solutions[currentSolutionIndex],metric1,metric2)):
                            toRemove.append(currentSolutionIndex)
                            break
                for discardedSolution in toRemove:
                    paretoCandidates.remove(discardedSolution)
                toRemove = []
        paretos = {} #mesma estrutura de self.solutions, só que só de paretos, para retornar
        for count,paretoSolutionIndex in enumerate(paretoCandidates):
            #não acho que precisa copiar, então vou só passar referencia(eles não deveriam ser modificados mesmo)
            paretos[count] = self.solutions[paretoSolutionIndex]
        return paretos