from heuristics.heuristic import Heuristic
from pathlib import Path
from domain.solution import Solution
from utils.Script_tcl import generateScriptWithInputIR
import copy
from os import environ
from lib.approxLib import *
import argparse
import shutil 

parser = argparse.ArgumentParser()
parser.add_argument('EXACT_DESIGN_BC', type=str, nargs=1)
parsed = parser.parse_args() 

EXACT_DESIGN_BC = parsed.EXACT_DESIGN_BC[0]
try:
    TRAINING_VECS_DIR = environ['TRAINING_VECS_DIR']
    TEST_VECS_DIR = environ['TEST_VECS_DIR']
except KeyError as error:
    print('Error: environment variable {} not defined.'.format(error.args[0]))
    raise

resultsDir = Path("approx_results")
exactDesignDir = resultsDir / "exact_design"
exactDesignProfilesDir = exactDesignDir / "profiles"
exactDesignOutputsDir = exactDesignDir / "outputs"
exactDesignTestOutputsDir = exactDesignOutputsDir / "test"
exactDesignTrainingOutputsDir = exactDesignOutputsDir / "training"
approxDesignsDir = resultsDir / "approx_designs"

if not resultsDir.exists():
    resultsDir.mkdir()
    exactDesignDir.mkdir()
    exactDesignProfilesDir.mkdir()
    exactDesignOutputsDir.mkdir()
    exactDesignTestOutputsDir.mkdir()
    exactDesignTrainingOutputsDir.mkdir()
    approxDesignsDir.mkdir()
trainingInputsDir = Path(TRAINING_VECS_DIR)
testInputsDir = Path(TEST_VECS_DIR)

class GreedyApprox(Heuristic): 
    def __init__(self,filesDict):
        super().__init__(filesDict)
        self.inputByteCode = filesDict["exactDesignUpdatedBytecodeFile"]
        self.trainingDataProfile = filesDict["dataStatsTraining"]
        llvmOpt = Path("/home/nikolas/Documents/llvm-project-7/llvm-7.0.0.src/mybuilddir/bin/opt")
        generateScriptWithInputIR(filesDict["cFile"],filesDict["prjFile"], self.inputByteCode, llvmOpt.as_posix())
        self.run()

    def run(self):
        """
        generate tcl script that uses input IR for synthesis
        for each operation:
            option = get the option (v2c or no v2c) that gets the min fitness
            select this option

        """ 
        appliedApproximations = dict.fromkeys(self.dictDir,'')
        bytecode = self.inputIR
        outputPath = Path("./")
        approximations = ["","v2c"]
        bestFitness =  float('inf')
        outputsDir = Path("./")
        for operation in (self.trainingDataProfile.keys()):
            approxOpDir = outputsDir / ("op_" + operation)
            approxOpDir.mkdir()

            approxOpTrainingOutputsDir = approxOpDir / "outputs/training"
            approxOpTrainingOutputsDir.mkdir(parents=True)
            for option in approximations:
                if option == "v2c":
                    try:
                        constantValue = getConstantValueFromStatistics(operation["grandMean"],operation["grandStdDev"], operation["operationBitwidth"])
                        bytecode = variableToConstantTransformation(self.inputIR, operation, constantValue, outputPath)
                    except Exception as e:
                        print(e)
                try:
                    solution:Solution = compileBytecode(bytecode,outputPath) 
                except Exception as e:
                    appliedApproximations[operation] = ''
                    print(e)
                approxDesignOutputsValues = getOutputsValues(bytecode, trainingInputsDir, approxOpTrainingOutputsDir, deleteOutputFiles=True)
                approxDesignMseValues = getMseValues(approxDesignOutputsValues, self.filesDict["goldenOutputsTraining"])
                meanMseValue = numpy.mean(list(approxDesignMseValues.values()), dtype=numpy.float64)
                currentFitness = self._fitness(meanMseValue, solution.results["resources"] * solution.results["latency"])   
                if currentFitness < bestFitness:
                    bestFitness = currentFitness
                    bestApproximationOption = option
            appliedApproximations[operation] = bestApproximationOption

    def _fitness(self,mseValue,resourcesXLatency):
        if mseValue == 0:
            return resourcesXLatency
        else:
            return resourcesXLatency / mseValue 
        



def main():

    print ('Info: compiling the exact design ...')
    exactDesignBytecodeFile = exactDesignDir / EXACT_DESIGN_BC
    shutil.copy(EXACT_DESIGN_BC,exactDesignBytecodeFile)
    try:
        exactDesignUpdatedBytecodeFile = updateBytecodeOpsMetadata(exactDesignBytecodeFile, exactDesignDir)
        exactDesignReportFiles = compileBytecode(exactDesignUpdatedBytecodeFile, exactDesignDir)
        #exactDesignOpsMetadataFile = getOpsMetadataFromBytecode(exactDesignUpdatedBytecodeFile, exactDesignReportFiles['scheduling'], exactDesignDir).
        goldenOutputsTest = getOutputsValues(exactDesignUpdatedBytecodeFile, testInputsDir, exactDesignTestOutputsDir, deleteOutputFiles=False)
        goldenOutputsTraining, dataStatsTraining = getOutputsValuesAndDataStats(exactDesignUpdatedBytecodeFile,
                                                                                trainingInputsDir,
                                                                                exactDesignTrainingOutputsDir,
                                                                                exactDesignProfilesDir, deleteOutputFiles=False)
    except RCApproxException:
        shutil.rmtree('./approx_results')
        print("Error: something went wrong when trying to profile the exact design.")
        raise
    filesDict = {}
    filesDict["exactDesignUpdatedBytecodeFile"] = exactDesignUpdatedBytecodeFile
    filesDict["solution"] = exactDesignReportFiles
    filesDict["goldenOutPutsTest"] = goldenOutputsTest
    filesDict["goldenOutputsTraining"] = goldenOutputsTraining
    filesDict["dataStatsTraining"] = dataStatsTraining
    heuristic = GreedyApprox(filesDict)
        
if __name__ == '__main__':
    main()
