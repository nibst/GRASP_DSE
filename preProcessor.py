import re


class PreProcessor():
    dataset = {} #será o dicionario de instrucoes
    
    def process(self,dataset):
        self.dataset = dataset
        featuresByColumn = self._takeColumns()
        return self.__directivesToNumbers(featuresByColumn)
    
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
        elif parameterType == 'dim':
            return int(parametersDict[parameterType]) + 1
        else:
            return 1

    def __divideIntoMoreColumns(self,parametersDict:dict,finalDict:dict,directiveType,count):
        for parameterType in parametersDict:
            key = directiveType + parameterType
            if key not in finalDict.keys():    
                finalDict[key] = [0]*len(self.dataset)  
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
             
    def __directivesToNumbers(self,featuresByColumn):
        regexForFlag = '\-[a-zA-Z]+\s[a-zA-Z0-9]*[^\s]' #pega as flags/parametros tipo: -factor 10, -dim 0, -type cyclic,etc
        finalDict = {} #terá as diretivas em forma de numero para poder aplicar random forest
        for directiveType in featuresByColumn:
            column =featuresByColumn[directiveType]
            newColumn = []
            count = 0 #conta em qual diretiva está atualmente
            for directive in column:
                if directive is None or directive == '':
                    featureValue = 0
                else:
                    parametersList = (re.findall(regexForFlag,directive))
                    parametersDict = self.__getParametersDict(parametersList)
                    if len(parametersList)>0:
                        self.__divideIntoMoreColumns(parametersDict,finalDict,directiveType,count)
                    else:
                        featureValue = 1
                newColumn.append(featureValue)
                count+=1
            finalDict[directiveType] = newColumn
        featuresVector = self.__toFeaturesVector(finalDict)
        return featuresVector

    def _takeColumns(self):
        columnsDict = {}
        featuresTypes = self.dataset[0].diretivas

        for directiveType in featuresTypes:
            featuresColumn = []
            for solutionIndex in range(len(self.dataset)):
                featuresColumn.append(self.dataset[solutionIndex].diretivas[directiveType])
            columnsDict[directiveType] = featuresColumn
        return columnsDict