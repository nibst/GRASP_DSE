import argparse
import time
from tkinter import EXCEPTION
from RandomSearch import RandomSearch
from estimator import Estimator
from heuristic import Heuristic
from pathlib import Path
from randomForest import RandomForestEstimator
from solution import Solution
from Script_tcl import generateScript
import copy
import random



class GRASP(Heuristic):
    
    
    #_SECONDS = 7200
    def __init__(self,filesDict,outPath,model:Estimator,seed=0):
        super().__init__(filesDict, outPath)
        self.alpha = 0.7
        sample = RandomSearch(filesDict, outPath)
        self.estimator = model
        self.estimator.trainModel(sample.solutions)
        
        self.dictDir =self.parsedTxt()
        random.seed(seed)
        self.createSolutionsDict()
       
    
    def createSolutionsDict(self,iterations=10):
        """
        procedure GRASP(Max Iterations,Seed)
            1 Read Input();
            2 for k = 1,...,Max Iterations do
                3 Solution ← Greedy Randomized Construction(Seed);
                4 if Solution is not feasible then
                    5 Solution ← Repair(Solution);
                6 end;
                7 Solution ← Local Search(Solution);
                8 Update Solution(Solution,Best Solution);
            9 end;
            10 return Best Solution;
        end GRASP.

        """
        for i in range(iterations):
            solution = self.constructGreedyRandomizedSolution()
            #repair solution?
            solution = self.localSearch(solution)

        generateScript(self.cFiles, self.prjFile)

    def makeRCL(self,directiveGroup:str,solutionToBuild:dict):
        """
        Enters in RCL if candidate resource X latency is below
        (1+alpha)*min(resourceXlatency of all canidates)
        """
        RCL = []
        candidates = [] 
        bestResourcesXLatency = float('inf')
        #take all candidates
        for directive in self.dictDir[directiveGroup]:
            solutionToBuild[directiveGroup] = directive
            candidate = Solution(solutionToBuild,self.cFiles,self.prjFile)
            estimatedResults = self.estimator.estimateSynthesis(candidate)
            candidate.setResultados(estimatedResults)
            candidates.append(candidate)
            resourcesXlatency=  candidate.resultados['resources'] * candidate.resultados['latency']
            if  resourcesXlatency < bestResourcesXLatency:
                bestResourcesXLatency = resourcesXlatency
        
        #create RCL from some or all candidates
        #RCL = {v E Vk | dv < (1 + alpha)*min(resourcesXlatency)}
        #v = candidate, Vk = candidates, dv = resourcesXlatency of candidate
        for candidate in candidates:
            resourcesXlatency=  candidate.resultados['resources'] * candidate.resultados['latency']
            if  resourcesXlatency < (1+self.alpha)*bestResourcesXLatency:
                #append only the directive string
                RCL.append(candidate.diretivas[directiveGroup])
        return RCL


    def constructGreedyRandomizedSolution(self):
        """
        procedure Greedy Randomized Construction(Seed)
            1 Solution ← /0;
            2 Initialize the set of candidate elements;
            3 Evaluate the incremental costs of the candidate elements;
            4 while there exists at least one candidate element do
                5 Build the restricted candidate list (RCL);
                6 Select an element s from the RCL at random;
                7 Solution ← Solution ∪ {s};
                8 Update the set of candidate elements;
                9 Reevaluate the incremental costs;
            10 end;
            11 return Solution;
        end Greedy Randomized Construction.
        """
        solutionToBuild = dict.fromkeys(self.dictDir,'') #Cria um dicionário 'diretivas' a partir do 'dictDir' mas 
                                                        #mantendo apenas os títulos das diretivas - seu valores são
                                                        #trocados por None
        directiveGroups = list(self.dictDir.keys())                                                
        random.shuffle(directiveGroups)
        for directiveGroup in directiveGroups:
            RCL = self.makeRCL(directiveGroup,solutionToBuild)
            s = random.choice(RCL)
            solutionToBuild[directiveGroup] = s
        constructedSolution = Solution(solutionToBuild,self.cFiles,self.prjFile)
        try:
            self.synthesisWrapper(constructedSolution)
        except Exception as error:
            print(error)
        else:
            self.estimator.trainModel(constructedSolution)

        return constructedSolution

        

    def localSearch(self,solution:Solution):
        neighbors = [] #in resources x latency
        
        for directiveGroup in self.dictDir.keys():
            neighborDirectives = copy.deepcopy(solution.diretivas)
            for directive in self.dictDir[directiveGroup]:
                if solution.diretivas[directiveGroup] != directive:
                    neighborDirectives[directiveGroup] = directive
                    neighborSolution = Solution(neighborDirectives,self.cFiles,self.prjFile)
                    estimatedResults = self.estimator.estimateSynthesis(neighborSolution)
                    neighborSolution.setResultados(estimatedResults)
                    neighbors.append(neighborSolution)
        
        neighborsSorted = sorted(neighbors,key=lambda k: k.resultados['resources'] * k.resultados['latency']) #sort in ascending order of resource X latency
        #synthesize top n neighbors, for now is top 1 synthesizable
        i=0
        synthesisCount = 0
        n = 1
        topSynthesis = []
        while i < len(neighborsSorted):
            try:
                self.synthesisWrapper(neighborsSorted[i])
            except Exception as error:
                print(error)
            else:
                synthesisCount+=1
                topSynthesis.append(neighborsSorted[i])
                if synthesisCount == n:
                    break
        
        topSolution = max(topSynthesis,key=lambda k: k.resultados['resources'] * k.resultados['latency'])    
        return topSolution


if __name__ == '__main__':
        
    #Initialize parser
    parser = argparse.ArgumentParser()

    # Adding argument
    parser.add_argument("-c", "--cFiles", help = "C input files list", required=True, nargs='+')
    parser.add_argument("-d", "--dFile", help = "Directives input file",required=True)
    parser.add_argument("-p", "--prjFile", help = "Prj. top file",required=True)

 
    # Read arguments from command line
    args = parser.parse_args()
    
    filesDict = {}
    filesDict['cFiles'] = args.cFiles
    filesDict['dFile'] = args.dFile
    filesDict['prjFile'] = args.prjFile
    model = RandomForestEstimator(filesDict['dFile'])
    grasp = GRASP(filesDict,'directives.tcl',model)