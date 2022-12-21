from abc import ABC, abstractmethod
import re
from domain.solution import Solution
import copy
import utils.readDirectivesFile as readDirectivesFile
from pathlib import Path
import json
import pickle


class Heuristic(ABC):

    #TODO colocar super().__init__(bla bla) em todas nossas heuristicas
    #TODO make solutions be a list of solutions instead of a dict
    def __init__(self,filesDict,outPath):
        self.filesDict = filesDict
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        with open(filesDict['dFile']) as jsonFile:
            self.DSEconfig:dict =  json.load(jsonFile)
        directivesDict = copy.deepcopy(self.DSEconfig['directives'])
        self.dictDir = {}
        for key in directivesDict:
            self.dictDir[key] = directivesDict[key]['possible_directives']
        self.solutionIndex = 0
        self.solutions = {}

    def parsedTxt(self):
        return readDirectivesFile.fileParser(self.directivesTxt)
    #Passa para o arquivo readDirectivesFile.py o texto lido do arquivo

    

    @abstractmethod                         # Método abstrato a sere herdados e implementado
    def createSolutionsDict(self):           # pelas classes filhas
        pass

    def writeToFile(self,filename):
        with open(filename, 'wb') as solutionsFile:
            pickle.dump(self, solutionsFile)

    def dominateInBothMetrics(self,Solution1,Solution2,metric1,metric2):
        #testa se a Solution1  domina a Solution2
        return ((Solution2.resultados[metric1]>=Solution1.resultados[metric1]) and (Solution2.resultados[metric2] >= Solution1.resultados[metric2]))
    def paretoSolutions(self,metric1,metric2,solutions=None ):

        if solutions == None:
            solutions = self.solutions
        """consegue as soluções que são dominadas por outras. Eliminas essas soluções, retorando só nas que são pareto
            Retorna um dicionário enumerado de paretos(soluções). Ex: paretos[0],paretos[1],etc. paretos[i] == algum objeto Solution"""
        toRemove = [] #armazena o indice da solução que deve ser eliminada
        paretoCandidates = [] #armazena indice das solucoes candidatas a pareto, é inicializada com todos indices
        solutionsIndex = []
        #inicializa
        for i in range(len(solutions)):
            paretoCandidates.append(i)
            solutionsIndex.append(i)
            
        for currentSolutionIndex in solutionsIndex:
            if currentSolutionIndex in paretoCandidates:
                for paretoSolutionIndex in paretoCandidates:
                    if currentSolutionIndex != paretoSolutionIndex:
                        #se current solution dominar a solucao candidate a pareto
                        if(self.dominateInBothMetrics(solutions[currentSolutionIndex],solutions[paretoSolutionIndex],metric1,metric2)):
                            toRemove.append(paretoSolutionIndex)
                        #se a solucao candidata a pareto dominar a current solution
                        elif(self.dominateInBothMetrics(solutions[paretoSolutionIndex],solutions[currentSolutionIndex],metric1,metric2)):
                            toRemove.append(currentSolutionIndex)
                            break
                for discardedSolution in toRemove:
                    paretoCandidates.remove(discardedSolution)
                toRemove = []
        paretos = {} #mesma estrutura de self.solutions, só que só de paretos, para retornar
        for count,paretoSolutionIndex in enumerate(paretoCandidates):
            #não acho que precisa copiar, então vou só passar referencia(eles não deveriam ser modificados mesmo)
            paretos[count] = solutions[paretoSolutionIndex]
        return paretos
    def countAllSpace(self):
        totalMultiplication = 1
        for directiveGroup in self.dictDir:
            totalMultiplication*=len(self.dictDir[directiveGroup])
        return totalMultiplication

    def countPrunnedSpace(self):
        totalMultiplication = 1
        directivesByLabel:dict = self.__buildLabelDict(self.dictDir)
        for item in directivesByLabel.values():
            if 'pipeline'  in item and 'unroll'  in item:
                mult = (len(item['pipeline']) * len(item['unroll'])) -1
                totalMultiplication*=mult
            else:
                for directiveList in item.values():
                    totalMultiplication*=len(directiveList)
        return totalMultiplication


    def __buildLabelDict(self,directives:dict):
        """
        Receives a directives dict that its keys are the group of directive and its values
        are the directives chosen to that group.(Normally its one directive chosen for one group)

        returns a dictionary that the keys are the spots of application of directives
        (the function where the label is + '/' + the name of label) and the values are
        all directives applied in that spot. Directives are divided by directive type
        Ex:
        newDict = {local_memset/local_memset_label0:
                    {
                        'pipeline':'some_directive'
                        'unroll': 'another_directive'
                    }
                }
        """
        newDict:dict = {}
        directivesInformation = self.DSEconfig['directives']
        for directiveGroup in directives:
            label = directivesInformation[directiveGroup]['label']
            function = directivesInformation[directiveGroup]['function']
            key = function + '/' + label
            directiveType = directivesInformation[directiveGroup]['directive_type']
            if key not in newDict:
                newDict[key] = {}
            newDict[key][directiveType] =directives[directiveGroup]
        return newDict

    #TODO maybe is a function of class Solution
    def isRedundantDesign(self,directives:dict):
        """
        verifies if a certain design have some redundancies with the applied directives
        
        If pipeline is active for a certain loop level, all its subloops are automatically unrolled. 
        Thus all design points that apply unroll pragmas to automatically unrolled loops are considered redundant and excluded.
        Moreover, all subloops with pipeline pragmas are discarded because of the effect described below:
        
        When a loop level l is fully unrolled, its logic is replicated for every iteration 
        and the loop structure itself ceases to exist. Therefore, we discard the points
        where pipeline is active for a fully unrolled level,
        since there will be no actual loop to implement pipeline in this case
        """
        directivesByLabel:dict = self.__buildLabelDict(directives)
        loopsInformation = self.DSEconfig['nested_loops']
        #check if a pipeline is applied to a fully unrolled loop 
        factorRegex = '\s-factor\s'
        for item in directivesByLabel.values():
            if 'pipeline' not in item or 'unroll' not in item:
                pass
            elif item['pipeline'] == '' or item['unroll'] == '':
                pass
            #if there isnt a factor argument on directive, then its fully unrolled    
            elif re.search(factorRegex,item['unroll']) is None:
                return True

        for loop in loopsInformation:
            #go to the most inner loop
            innerLoop = loop
            function = loop['function']
            pipelineLoop=None
            #get the loop that has pipeline active, if any
            while innerLoop['nest']:
                label = innerLoop['label']
                key = function + '/' + label
                item = directivesByLabel[key]
                #if loop has pipeline
                if 'pipeline' in item and item['pipeline'] != '':
                    pipelineLoop = innerLoop
                    break
                innerLoop = innerLoop['nest']

            #check if any of the subloops,of pipelined loop, has unroll or pipeline
            if pipelineLoop is not None:
                innerLoop = pipelineLoop
                while innerLoop['nest']:
                    innerLoop = innerLoop['nest']
                    label = innerLoop['label']
                    key = function + '/' + label
                    item = directivesByLabel[key]
                    #if inner loop has pipeline or unroll, return true
                    if 'pipeline'in item or 'unroll' in item:
                        if item['pipeline'] != '' or item['unroll'] != '':
                            return True
        return False 


    def getCachedSoltuion(self,solution:Solution):
        """
        get especified solution from self.solutions if it exists.
        check tree of solution directives to know if solution exists already in self.solutions
        """
        pass

    def saveSolution(self,solution):
        deep = copy.deepcopy(solution)   
        #if get cached solution
        #   use cached solution
        #else add solution to tree and add solutin to self.solution
        self.solutions[self.solutionIndex] = deep               
        self.solutionIndex+=1


    def synthesisWrapper(self,solution:Solution,timeLimit=None):
        """
        Calls synthesis and, if its successful, it saves solution in self.solutions.
        """
        try:
            solution.runSynthesisTeste(timeLimit)
        except Exception as e:
            raise
        else:
            self.saveSolution(solution)
            