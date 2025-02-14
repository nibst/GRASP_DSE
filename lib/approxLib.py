from os import environ
from pathlib2 import Path
from math import sqrt
import subprocess
import numpy  
from domain.designToolFactory import DesignToolFactory
from domain.solution import Solution
from math import floor, ceil, sqrt, log

from utils.Script_tcl import generateScriptWithInputIR

VERBOSE = True

try:
    RCAPPROX_LLVM_LIB = environ['RCAPPROX_LLVM_LIB']
    RCAPPROX_LIB_DIR = environ['RCAPPROX_LIB_DIR']
    TIMEOUT = environ['TIMEOUT']
    BENCH_IOLIB_DIR = environ['BENCH_IOLIB_DIR']
    LLVM_OPT = environ['LLVM_OPT']
    CLANG = environ['CLANG']
    LLVM_LLI = environ['LLVM_LLI']
    LLVM_LINK = environ['LLVM_LINK']
except KeyError as error:
    print('Error: environment variable {} not defined.'.format(error.args[0]))
    raise



class RCApproxException(Exception):
    pass

class MetadataUpdateError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to update operations metadata of {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))

class InstrumentationError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to instrument {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))

class ExecutionError(RCApproxException):
    def __init__(self, bytecode, inputFile, errorCode, output):
        self.bytecode = bytecode
        self.inputFile = inputFile
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to execute {} with input {}. Error code: {}. stderr: {}.'
                        .format(bytecode, inputFile, errorCode, output))

class CompilationError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to compile {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))

class IOFunctionCallLinkError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to link I/O function calls on {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))

class MetadataReadError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to get operations metadata from {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))

class Variable2ConstantTransformationError(RCApproxException):
    def __init__(self, bytecode, operation, constantValue, errorCode, output):
        self.bytecode = bytecode
        self.operation = operation
        self.constantValue = constantValue
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to substitute operation {} with constant value {} on {}. Error code: {}. stderr: {}.'
                        .format(operation, constantValue, bytecode,errorCode, output))

class OptimizationError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to optimize {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))

class ResourcesUsageReadError(RCApproxException):
    def __init__(self, bytecode, errorCode, output):
        self.bytecode = bytecode
        self.errorCode = errorCode
        self.output = output
        super().__init__('failed to get resources usage from {}. Error code: {}. stderr: {}.'
                        .format(bytecode, errorCode, output))		

def printMessage(message: str, end='\n', flush=False) -> None:
    
    if(VERBOSE):
        print(message, end=end, flush=flush)


def updateBytecodeOpsMetadata(bytecodeFile: Path, outputDir: Path) -> Path:

    assert (bytecodeFile.is_file() and outputDir.is_dir())

    printMessage('Updating operations metadata of {} ... '.format(bytecodeFile.as_posix()), end="", flush=True)

    updatedBytecodeFile = outputDir / (bytecodeFile.stem + ".MDUpdated.bc")
    updateMetadataCmd = (LLVM_OPT + " -load " + RCAPPROX_LLVM_LIB +
                         " -updateMD < " + bytecodeFile.as_posix() +
                        " > " + updatedBytecodeFile.as_posix())

    try: 
        subprocess.check_output(updateMetadataCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise MetadataUpdateError(bytecodeFile.as_posix(), error.returncode, error.output) 

    printMessage('Done! New bytecode saved in {}: {}'.format(outputDir.as_posix(), updatedBytecodeFile.name))

    return updatedBytecodeFile

def getOpsMetadataFromBytecode(bytecodeFile: Path, legupSchedulingRptFile: Path, outputDir: Path) -> Path:

    assert (bytecodeFile.is_file() and legupSchedulingRptFile.is_file() and outputDir.is_dir())
    DEVICE_CHAR_FILE = ""
    printMessage('Getting operations metadata from {} ... '.format(bytecodeFile.as_posix()), end="", flush=True)

    opsMetadataFile = outputDir / (bytecodeFile.stem + ".metadata.txt")
    getOpsMetadataCmd = (LLVM_OPT + " -load " + RCAPPROX_LLVM_LIB +
                " -resourcesEval -sr " + legupSchedulingRptFile.as_posix() +
                " -cf " + DEVICE_CHAR_FILE +
                " -of " + opsMetadataFile.as_posix() +
                " < " + bytecodeFile.as_posix() +
                " > /dev/null")
    try: 
        subprocess.check_output(getOpsMetadataCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise MetadataReadError(bytecodeFile.as_posix(), error.returncode, error.output) 

    printMessage('Done! New metadata saved in {}: {}'.format(outputDir.as_posix(), opsMetadataFile.name))
    
    return opsMetadataFile


def compileBytecode(bytecodeFile: Path, outputsDir: Path, filesDict = None) -> dict:

    assert (bytecodeFile.is_file() and outputsDir.is_dir())

    printMessage('Compiling bytecode {} (this process may take several minutes) ... '.format(bytecodeFile.as_posix()), end="", flush=True)
    
    IOFunctionCallRemovedBytecodeFile = outputsDir / (bytecodeFile.stem + ".IOFCallRemoved.bc")
    
    # remove instrumented IO function calls if present 
    removeIOFunctionCallCmd = (LLVM_OPT + " -load " + RCAPPROX_LLVM_LIB +
                                " -removeIOFCall -dce < " +	bytecodeFile.as_posix() +
                                " > " + IOFunctionCallRemovedBytecodeFile.as_posix() + ";")
    
    try:
        subprocess.check_output(removeIOFunctionCallCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise CompilationError(bytecodeFile.as_posix(), error.returncode, error.output) 
    if(filesDict):
        generateScriptWithInputIR(filesDict["cFiles"],filesDict["prjFile"],IOFunctionCallRemovedBytecodeFile.as_posix(),LLVM_OPT)
    designTool = DesignToolFactory().getDesignTool('vitis')
    solution = Solution({})
    try:
        solution = designTool.runSynthesis(solution)
    except Exception as e:
        raise
    return solution
    
def getMseValues(outputsValues: dict, goldenOutputsValues: dict) -> dict:
    
    assert outputsValues.keys() == goldenOutputsValues.keys()

    mseValues = dict()

    for output, values in outputsValues.items():
        squaredDifferences = numpy.square(numpy.array(goldenOutputsValues[output])-numpy.array(values))
        mseValues[output] = numpy.mean(squaredDifferences, dtype=numpy.float64)

    return mseValues

def linkIOFunctionCall(bytecodeFile: Path, outputDir: Path) -> Path:
    IOLinkedBytecodeFile = outputDir / (bytecodeFile.stem + ".IOLinked.bc")
    

    linkIOFunctionCallCmd = (LLVM_LINK + " -o " + IOLinkedBytecodeFile.as_posix() +
                            " " + bytecodeFile.as_posix() +
                            " " + BENCH_IOLIB_DIR + "populateIO.bc;")
    try: 
        subprocess.check_output(linkIOFunctionCallCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise IOFunctionCallLinkError(bytecodeFile.as_posix(), error.returncode, error.output) 
    return IOLinkedBytecodeFile


def instrumentBytecode(bytecodeFile: Path, dataStatsFile: Path, outputDir: Path) -> Path:

    instrumentedBytecodeFile = outputDir / (bytecodeFile.stem + ".instrumented.bc")
    
    instrumentationCmd = (LLVM_OPT + " -load " + RCAPPROX_LLVM_LIB +
                            " -profiling -pf " + dataStatsFile.as_posix() +
                            " < " + bytecodeFile.as_posix() +
                            " > " + instrumentedBytecodeFile.as_posix() + ";")

    linkedBytecodeFile = outputDir / (instrumentedBytecodeFile.stem + ".Linked.bc")

    linkProfileFCallCmd = (LLVM_LINK + " -o " + linkedBytecodeFile.as_posix() +
                            " " + instrumentedBytecodeFile.as_posix() +
                            " " + RCAPPROX_LIB_DIR + "profiler.bc")
    
    try: 
        subprocess.check_output(instrumentationCmd + linkProfileFCallCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise InstrumentationError(bytecodeFile.as_posix(), error.returncode, error.output)
    
    return linkedBytecodeFile

def executeBytecode(bytecodeFile: Path, inputFile: Path, outputDir: Path) -> Path:

    outputFile = outputDir / (inputFile.stem + ".output.txt")
    executableFile = "a.out"
    compileCmd = ("timeout -k 5 " + TIMEOUT + " " +
                    CLANG + " " + bytecodeFile.as_posix() + " -lm " +  "-o " + executableFile + "; ")
    executionCmd = ("./" + executableFile + " " + inputFile.as_posix() + " " + outputFile.as_posix())
    try: 
        subprocess.check_output(compileCmd, stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output(executionCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise ExecutionError(bytecodeFile.as_posix(), inputFile.as_posix(), error.returncode, error.output) from error
    return outputFile

def variableToConstantTransformation(bytecodeFile: Path, operation: str, constantValue: str, outputDir: Path) -> Path:

    assert (bytecodeFile.is_file() and outputDir.is_dir())

    printMessage('Replacing operation {} of {} by constant value {} ... '.format(operation, bytecodeFile.as_posix(), constantValue), end="", flush=True)
    
    variable2ConstantTransformedBytecodeFile = outputDir / (bytecodeFile.stem + ".pruned_" + operation + ".bc")
    
    variable2ConstantCmd = (LLVM_OPT + " -load " + RCAPPROX_LLVM_LIB +
                            " -pruning -opID " + operation +
                            " -opValue " + constantValue +
                            " < " + bytecodeFile.as_posix() +
                             " > " + variable2ConstantTransformedBytecodeFile.as_posix())
                             
    try:
        subprocess.check_output(variable2ConstantCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise Variable2ConstantTransformationError(bytecodeFile.as_posix(), operation, constantValue, error.returncode, error.output)

    printMessage('Done! Approximated bytecode saved in {}: {}'.format(outputDir.as_posix(), variable2ConstantTransformedBytecodeFile.as_posix()))
    
    return variable2ConstantTransformedBytecodeFile

def optimizeBytecode(bytecodeFile: Path, outputDir: Path) -> Path:

    assert (bytecodeFile.is_file() and outputDir.is_dir())

    printMessage('Optimizing bytecode {} (dead code elimination, constant propagation, and instruction combine) ... '.format(bytecodeFile.as_posix()), end="", flush=True)

    optimizedBytecodeFile = outputDir / (bytecodeFile.stem + ".optimized.bc")
    
    optimizeCmd = (LLVM_OPT + " -dce -constprop -instcombine -instnamer < " + bytecodeFile.as_posix() +
                    " > " + optimizedBytecodeFile.as_posix())
                    
    try:
        subprocess.check_output(optimizeCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise OptimizationError(bytecodeFile.as_posix(), error.returncode, error.output) 
    
    printMessage('Done! Optimized bytecode saved in {}: {}'.format(outputDir.as_posix(), optimizedBytecodeFile.as_posix())) 
    
    return optimizedBytecodeFile


def getOutputsValues(bytecodeFile: Path, inputsDir: Path, outputsDir: Path, deleteOutputFiles=False) -> dict:
    
    assert (bytecodeFile.is_file() and inputsDir.is_dir() and outputsDir.is_dir())

    printMessage('Executing {} to get output values (this process may take several minutes) ... '.format(bytecodeFile.as_posix()), end="", flush=True)

    outputsValues = dict()

    try:
        IOLinkedBytecodeFile = linkIOFunctionCall(bytecodeFile, outputsDir)
    except RCApproxException: raise
    
    for inputFile in inputsDir.glob('*.txt'):
        try:
            outputFile = executeBytecode(IOLinkedBytecodeFile, inputFile, outputsDir)
        except RCApproxException: raise
        
        outputsValues[outputFile.stem] = [float(value) for value in outputFile.read_text().splitlines()]
        
    if deleteOutputFiles:
        for outputFile in outputsDir.glob('*.txt'):
            outputFile.unlink()
        printMessage('Done!') 
    #else:
        printMessage('Done! Output files saved in {}'.format(outputsDir.as_posix())) 

    return outputsValues

def getOutputsValuesAndDataStats(bytecodeFile: Path, inputsDir: Path, outputsDir: Path, dataStatsDir: Path, deleteOutputFiles=False) -> (dict, dict):

    assert (bytecodeFile.is_file() and inputsDir.is_dir() and outputsDir.is_dir() and dataStatsDir.is_dir())
    
    printMessage('Executing {} to get output values and data statistics (this process may take several minutes) ... '.format(bytecodeFile.as_posix()), end="", flush=True)
    
    dataStatsFile = dataStatsDir / (bytecodeFile.stem + ".stats.txt")
    
    try:
        instrumentedBytecodeFile = instrumentBytecode(bytecodeFile, dataStatsFile, dataStatsDir)
        instrumentedIOLinkedBytecodeFile = linkIOFunctionCall(instrumentedBytecodeFile, dataStatsDir)
    except RCApproxException: raise
    
    outputValues = dict()
    dataStats = dict()
    
    for inputFile in inputsDir.glob("*.txt"):
        try:
            outputFile = executeBytecode(instrumentedIOLinkedBytecodeFile, inputFile, outputsDir)
        except ExecutionError: raise
    
        outputValues[outputFile.stem] = [float(value) for value in outputFile.read_text().splitlines()]

        # replace stats file according to the input vector
        opDataStatsFile = dataStatsDir / (inputFile.stem + ".stats.txt")
        dataStatsFile.replace(opDataStatsFile)
        
        for line in opDataStatsFile.read_text().splitlines():
            fields = line.split('|')
            operation = fields[0]
            if operation not in dataStats:
                dataStats[operation] = {'inputs': 1,
                                        'bitwidth': int(fields[4]),
                                        'execCount': int(fields[5]),
                                        'grandMean': float(fields[6]),
                                        'sumOfSquared': float(fields[9]),
                                        'grandStdDev': 0}
            else:
                dataStats[operation]['inputs'] += 1
                dataStats[operation]['grandMean'] += ((float(fields[6]) - dataStats[operation]['grandMean']) / dataStats[operation]['inputs'])
                dataStats[operation]['execCount'] += float(fields[5])
                dataStats[operation]['sumOfSquared'] += float(fields[9])
                
    statsInfo = str()
    for operation in dataStats:
        # calculate the grand standard deviation
        dataStats[operation]['grandStdDev'] = (sqrt((1 / (dataStats[operation]['execCount'] - 1)) *
                                            (dataStats[operation]['sumOfSquared'] -
                                            ((dataStats[operation]['grandMean'] ** 2) *
                                            (dataStats[operation]['execCount'])))))
        # save statistics information
        statsInfo += ('{}|{}|{}|{}|{}|{}|{}\n'.format(
                    operation,
                    dataStats[operation]['bitwidth'],
                    dataStats[operation]['inputs'],
                    dataStats[operation]['execCount'],
                    dataStats[operation]['grandMean'],
                    dataStats[operation]['sumOfSquared'],
                    dataStats[operation]['grandStdDev']))
    
    if deleteOutputFiles:
        for outputFile in outputsDir.glob('*.txt'):
            outputFile.unlink()
        for outputFile in dataStatsDir.glob('*.txt'):
            outputFile.unlink()
        printMessage('Done!')
    else:
        overallDataStatsFile = dataStatsDir / (bytecodeFile.stem + ".overallDataStats.txt")
        overallDataStatsFile.write_text(statsInfo)
        printMessage('Done! Output files saved in {} and data statistics saved in {}'.format(outputsDir.as_posix(), dataStatsDir.as_posix()))
        
    return outputValues, dataStats	

def getConstantValueFromStatistics(grandMean: float, grandStdDev: float, operationBitwidth: int) -> int:

	intervalFloor = grandMean - grandStdDev
	intervalCeil = grandMean + grandStdDev 

	if intervalFloor <=  0 <= intervalCeil: # variable to zero
			return 0
	else:
		wrapAround = 0 if grandMean > 0 else 2 ** operationBitwidth
		nextPowerOf2 = 2 ** (ceil(log(grandMean + wrapAround, 2))) 
		previousPowerOf2 = 2 ** (floor(log(grandMean + wrapAround, 2)))
		nearestPowerOf2 = previousPowerOf2 if (grandMean - previousPowerOf2) <= (nextPowerOf2 - grandMean) else nextPowerOf2

		if intervalFloor <= nearestPowerOf2 <= intervalCeil: # variable to power of 2
			return nearestPowerOf2
		else: # variable to mean
			return grandMean 
        
def getMseValues(outputsValues: dict, goldenOutputsValues: dict) -> dict:
	
	assert outputsValues.keys() == goldenOutputsValues.keys()

	mseValues = dict()

	for output, values in outputsValues.items():
		squaredDifferences = numpy.square(numpy.array(goldenOutputsValues[output])-numpy.array(values))
		mseValues[output] = numpy.mean(squaredDifferences, dtype=numpy.float64)

	return mseValues