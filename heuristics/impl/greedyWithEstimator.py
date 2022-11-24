from heuristics.heuristic import Heuristic
from pathlib import Path
from domain.solution import Solution
from utils.Script_tcl import generateScript
import copy
from heuristics.impl.RandomSearch import RandomSearch
from predictor.preprocessing.preProcessor import PreProcessor
from sklearn.model_selection import train_test_split
from predictor.estimators.randomforest.randomForest import RandomForestEstimator
class GreedyWithEstimator(Heuristic):
    
    
    
    def __init__(self,filesDict,outPath):
        self.directivesTxt = Path(filesDict['dFile']).read_text()
        self.cFiles = filesDict['cFiles']
        self.prjFile = filesDict['prjFile']
        self.outPath = outPath
        
        sample = RandomSearch(filesDict, outPath)
        processor = PreProcessor(filesDict['dFile'])
        train, test = train_test_split(sample.solutions, test_size=0.3,random_state=0)
        processedFeatures, processedResults = processor.process(train)
        self.rf = RandomForestEstimator(filesDict['dFile'])
        self.rf.trainModel(train)
        ls = self.rf.estimateSynthesis(test)
        score = self.rf.score(test)
        print(score)
        
        self.solutions = self.createSolutionsDict()
    #Atributos dos caminhos dos arquivos de entrada e saída.
    #Gera soluções conforme métodos abaixo e as salva numa lista em solutions

    
    def createSolutionsDict(self):
        
        dictDir=self.parsedTxt() 
        solutionsDict = {}
        
        final = dict.fromkeys(dictDir,None) #Cria um dicionário 'final' a partir do 'dictDir' mas 
                                                #mantendo apenas os títulos das diretivas - seu valores são
                                                #trocados por None
        solutionIndex=0
        generateScript(self.cFiles, self.prjFile)
        
        for diretiva in dictDir: 
            currentBest = None
            bestLUTxLatency = float('inf') #infinito
            
            for option in dictDir[diretiva]:   
                
                
                if option == '':
                    option = None

                final[diretiva] = option                             #Progressivamente popula o dicionário 'final' e cria
                estimatedSolution = Solution(final,self.cFiles,self.prjFile)         #Solutions a partir deste     
                estimatedResults = self.rf.estimateSynthesis(estimatedSolution)
                estimatedSolution.setResultados(estimatedResults[0])
                
                print(estimatedSolution.resultados)             
                lutXLatency = estimatedSolution.resultados['LUT'] * estimatedSolution.resultados['latency']
                if lutXLatency<bestLUTxLatency:          #mantendo aquelas onde o nro de LUTs é estritamente
                    bestLUTxLatency = lutXLatency
                    currentBest = option        #menor que o da anterior.
            
            final[diretiva] = currentBest
            solution = Solution(final,self.cFiles,self.prjFile)   
            try:
                solution.runSynthesis()
            except Exception as e:
                final[diretiva] = None #retira a diretiva usada
                print(e)
            #executa else qnd try roda sem erros    
            else:
                print(solution.resultados)
                deep = copy.deepcopy(solution)   
                solutionsDict[solutionIndex] = deep               
                solutionIndex+=1     
                           
            # Retorna o dicionário de soluções para o 'main'
        print(f'score: {self.rf.score(solution)}')
        return solutionsDict
