import json
import re
from domain.solution import Solution
class PreProcessor():
    dataset = {} #será o dicionario de solucoes
    def __init__(self,directivesFile) -> None:
        with open(directivesFile) as jsonFile:
            self.DSEconfig:dict =  json.load(jsonFile)
        directivesDict = self.DSEconfig['directives']
        self.possibleDirectives: dict = {}
        for key in directivesDict:
            self.possibleDirectives[key] = directivesDict[key]['possible_directives']

    def process(self,dataset):

        if isinstance(dataset, Solution):
            solutionToLst = []
            solutionToLst.append(dataset)
            dataset = solutionToLst
        if dataset == None:
            raise Exception("**ERROR DATASET IS EMPTY**")
        self.dataset = dataset
        featuresByColumn = self.__takeColumns()
        processedResults = self.__extractResults()
        possibleColumns = self.__buildColumns()
        processedFeatures = self.__directivesToNumbers(featuresByColumn,possibleColumns)
        return processedFeatures, processedResults
    
    def __buildColumns(self):
        """
        for each directive: build one or more columns
        """
        regexForParameter = '\-[a-zA-Z]+\s[a-zA-Z0-9]*[^\s]' #pega as flags/parametros tipo: -factor 10, -dim 0, -type cyclic,etc
        columnsNames = []
        for directiveType in self.possibleDirectives:
            columnsNames.append(directiveType)
            for directive in self.possibleDirectives[directiveType]:
                parametersList = (re.findall(regexForParameter,directive))
                parametersDict = self.__getParametersDict(parametersList)
                if len(parametersList)>0:
                    for parameterType in parametersDict:
                        key = directiveType + parameterType
                        if key not in columnsNames:
                            columnsNames.append(key)
        return columnsNames

    def __decide(self,parameterType,parametersDict):
        if parameterType == 'factor':
            return int(parametersDict[parameterType])
        elif parameterType == 'type':
            if parametersDict[parameterType] == 'block':
                return 1
            elif parametersDict[parameterType] == 'cyclic':
                return 2
            elif parametersDict[parameterType] == 'complete':
                return 3
            else: 
                return 1
        elif parameterType == 'dim':
            return int(parametersDict[parameterType]) + 1
        else:
            return 1

    def __divideIntoMoreColumns(self,parametersDict:dict,finalDict:dict,directiveType,count):
        for parameterType in parametersDict:
            key = directiveType + parameterType
            if len(finalDict[key]) == 0:    
                finalDict[key] = [-1]*len(self.dataset)  
            finalDict[key][count] = self.__decide(parameterType,parametersDict)
            
    def __getParametersDict(self,parametersList):
        parametersDict = {}
        for parameter in parametersList:
            splitting = parameter.split()
            parameterType = splitting[0][1:]                       #pega o primeiro do split [0] e tira o hifen do parameter type [1:]     
            parametersDict[parameterType] = splitting[1]           #e.g. dicionario[factor] = ["100"]
        return parametersDict

    def __toFeaturesVector(self, featuresByColumnDict):
        featuresVector = []
        #pegar o primeiro elemento de cada coluna de feature para formar alinha de feature
        keys = list(featuresByColumnDict.keys())
        for i in range(len(featuresByColumnDict[keys[0]])):
            solutionVector = []
            for key in featuresByColumnDict:
                solutionVector.append(featuresByColumnDict[key][i]) 
            featuresVector.append(solutionVector)       
        return featuresVector
             
    

    def __directivesToNumbers(self,featuresByColumn,possibleColumns):
        regexForParameter = '\-[a-zA-Z]+\s[a-zA-Z0-9]*[^\s]' #pega as flags/parametros tipo: -factor 10, -dim 0, -type cyclic,etc
        finalDict = {} #terá as diretivas em forma de numero para poder aplicar random forest
        #inicializar o dict com todas possiveis keys de colunas de features
        for columnKey in possibleColumns:
            finalDict[columnKey] = [] 
        for directiveType in featuresByColumn:
            column =featuresByColumn[directiveType]
            newColumn = []
            count = 0 #conta em qual diretiva está atualmente
            for directive in column:
                if directive is None or directive == '':
                    featureValue = -1
                else:
                    parametersList = (re.findall(regexForParameter,directive))
                    parametersDict = self.__getParametersDict(parametersList)
                    if len(parametersList)>0:
                        self.__divideIntoMoreColumns(parametersDict,finalDict,directiveType,count)
                        featureValue = 0
                    else:
                        featureValue = 1
                if featureValue == None:
                    print('a')
                newColumn.append(featureValue)
                count+=1
            finalDict[directiveType] = newColumn
        finalDict = self.__fillEmptyColumns(finalDict)
        featuresVector = self.__toFeaturesVector(finalDict)
        return featuresVector

    def __fillEmptyColumns(self,featuresByColumnDict:dict):
        for column in featuresByColumnDict.values():
            #se a lista/coluna for vazia encher ela
            if len(column) == 0:
                for i in range(len(self.dataset)):
                    column.append(0)
        return featuresByColumnDict

    def __takeColumns(self):
        columnsDict = {}
        featuresTypes = self.dataset[0].directives

        for directiveType in featuresTypes:
            featuresColumn = []
            for solutionIndex in range(len(self.dataset)):
                featuresColumn.append(self.dataset[solutionIndex].directives[directiveType])
            columnsDict[directiveType] = featuresColumn
        return columnsDict

    def __extractResults(self):
        results = []
        for solutionIndex in range(len(self.dataset)):
            solutionResults = []
            for metric in self.dataset[solutionIndex].results:
                solutionResults.append(self.dataset[solutionIndex].results[metric])
            results.append(solutionResults)
        #print(results)
        return results