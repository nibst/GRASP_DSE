from os import environ
from pathlib2 import Path
from math import floor, ceil, sqrt, log
import subprocess
import numpy  
import re
import itertools

try:
    DESIGN_NAME = environ['NAME']
    RCAPPROX_LLVM_LIB = environ['RCAPPROX_LLVM_LIB']
    RCAPPROX_LIB_DIR = environ['RCAPPROX_LIB_DIR']
    BENCH_IOLIB_DIR = environ['BENCH_IOLIB_DIR']
    DEVICE_CHAR_FILE = environ['DEVICE_CHAR_FILE']
    TIMEOUT = environ['TIMEOUT']
    OUTPUT_BITWIDTH = int(environ['OUTPUT_BITWIDTH'])
    MAX_BRANCHES = int(environ['MAX_BRANCHES'])
    VERBOSE = int(environ['VERBOSE'])
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

def getDesignResourcesFromFile(resourcesUsageFile: Path) -> (int, int, int):

    assert resourcesUsageFile.is_file()

    printMessage('Getting design resources (LUTs, REGs, and DSPs) from {} ... '.format(resourcesUsageFile.as_posix()), end="", flush=True)

    try:
        resources = resourcesUsageFile.read_text().splitlines()
    except FileNotFoundError as error:
        raise ResourcesUsageReadError(resourcesUsageFile.as_posix(), error.returncode, error.output)
        
    LUTs = int(re.sub(r'^LUTs: ', '', resources[0]))   
    REGs = int(re.sub(r'^REGs: ', '', resources[1]))
    DSPs = int(re.sub(r'^DSPs: ', '', resources[2]))
    
    printMessage('Done! LUTs:{}  REGs:{}  DSPs:{}'.format(LUTs, REGs, DSPs))
    
    return LUTs, REGs, DSPs

def updateBytecodeOpsMetadata(bytecodeFile: Path, outputDir: Path) -> Path:

	assert (bytecodeFile.is_file() and outputDir.is_dir())

	printMessage('Updating operations metadata of {} ... '.format(bytecodeFile.as_posix()), end="", flush=True)

	updatedBytecodeFile = outputDir / (bytecodeFile.stem + ".MDUpdated.bc")
	updateMetadataCmd = ("opt -load " + RCAPPROX_LLVM_LIB +
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

	printMessage('Getting operations metadata from {} ... '.format(bytecodeFile.as_posix()), end="", flush=True)

	opsMetadataFile = outputDir / (bytecodeFile.stem + ".metadata.txt")
	getOpsMetadataCmd = ("opt -load " + RCAPPROX_LLVM_LIB +
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

def compileBytecode(bytecodeFile: Path, outputsDir: Path) -> dict:

    assert (bytecodeFile.is_file() and outputsDir.is_dir())

    printMessage('Compiling bytecode {} (this process may take several minutes) ... '.format(bytecodeFile.as_posix()), end="", flush=True)
    
    IOFunctionCallRemovedBytecodeFile = outputsDir / (bytecodeFile.stem + ".IOFCallRemoved.bc")
    
    # remove instrumented IO function calls if present (not synthesizable)
    removeIOFunctionCallCmd = ("opt -load " + RCAPPROX_LLVM_LIB +
                                " -removeIOFCall -dce < " +	bytecodeFile.as_posix() +
                                " > " + IOFunctionCallRemovedBytecodeFile.as_posix() + ";")
	# Legup's compilation (verilog)
    legupCompilationCmd = "make backend BYTECODE=" + IOFunctionCallRemovedBytecodeFile.as_posix() + ";"
    # Quartus compilation (map, fitter, and netlist reports)
    quartusCompilationCmd = "make p f nwriter;"
    # generate resources usage and optimization reports from Quartus reports
    reportsParserCmd = "quartus_sh -t " + RCAPPROX_LIB_DIR + "reportParser.tcl;"
	
    try:
        subprocess.check_output(removeIOFunctionCallCmd + legupCompilationCmd + quartusCompilationCmd +
                                reportsParserCmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        raise CompilationError(bytecodeFile.as_posix(), error.returncode, error.output) 
	
    reportFiles = {'map': outputsDir / (bytecodeFile.stem + ".map.rpt"),
	                'fit': outputsDir / (bytecodeFile.stem + ".fit.rpt"),
				    'resources': outputsDir / (bytecodeFile.stem + ".resources.txt"),
					'mergedRegs': outputsDir / (bytecodeFile.stem + ".mergedRegs.txt"),
					'removedRegs': outputsDir / (bytecodeFile.stem + ".removedRegs.txt"),
					'duplicatedRegs': outputsDir / (bytecodeFile.stem + ".duplicatedRegs.txt"),
					'packedRegs': outputsDir / (bytecodeFile.stem + ".packedRegs.txt"),
					'netlist': outputsDir / (bytecodeFile.stem + ".netlist.vo"),
					'verilog': outputsDir / (bytecodeFile.stem + ".v"),
					'scheduling': outputsDir / (bytecodeFile.stem + ".scheduling.legup.rpt")}
                    
    Path("top.map.rpt").replace(reportFiles['map'])
    Path("top.fit.rpt").replace(reportFiles['fit'])
    Path("resourcesUsage.txt").replace(reportFiles['resources'])
    Path("mergedRegs.txt").replace(reportFiles['mergedRegs'])
    Path("removedRegs.txt").replace(reportFiles['removedRegs'])
    Path("duplicatedRegs.txt").replace(reportFiles['duplicatedRegs'])
    Path("packedRegs.txt").replace(reportFiles['packedRegs'])
    Path("simulation/modelsim/top.vo").replace(reportFiles['netlist'])
    Path(DESIGN_NAME + ".v").replace(reportFiles['verilog'])
    Path("scheduling.legup.rpt").replace(reportFiles['scheduling'])

    printMessage('Done! Report files saved in {}'.format(outputsDir.as_posix()))
    
    return reportFiles
    
def getMseValues(outputsValues: dict, goldenOutputsValues: dict) -> dict:
	
	assert outputsValues.keys() == goldenOutputsValues.keys()

	mseValues = dict()

	for output, values in outputsValues.items():
		squaredDifferences = numpy.square(numpy.array(goldenOutputsValues[output])-numpy.array(values))
		mseValues[output] = numpy.mean(squaredDifferences, dtype=numpy.float64)

	return mseValues

def getPsnrValues(outputsValues: dict, goldenOutputsValues: dict) -> dict:

	assert outputsValues.keys() == goldenOutputsValues.keys()
	
	psnrValues = dict()
	
	for output, values in outputsValues.items():
		squaredDifferences = numpy.square(numpy.array(goldenOutputsValues[output])-numpy.array(values))
		rmseValue = numpy.sqrt(numpy.mean(squaredDifferences, dtype=numpy.float64), dtype=numpy.float64)
		#valueRange = max(goldenOutputsValues[output]) - min(goldenOutputsValues[output]) 
		if rmseValue == 0:
			psnrValues[output] = numpy.inf
		else:
			psnrValues[output] = 20 * numpy.log10((2**OUTPUT_BITWIDTH - 1) / rmseValue, dtype=numpy.float64)

	return psnrValues

def linkIOFunctionCall(bytecodeFile: Path, outputDir: Path) -> Path:

	IOLinkedBytecodeFile = outputDir / (bytecodeFile.stem + ".IOLinked.bc")

	linkIOFunctionCallCmd = ("llvm-link -o " + IOLinkedBytecodeFile.as_posix() +
				            " " + bytecodeFile.as_posix() +
				            " " + BENCH_IOLIB_DIR + "populateIO.bc;")
	try: 
		subprocess.check_output(linkIOFunctionCallCmd, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as error:
		raise IOFunctionCallLinkError(bytecodeFile.as_posix(), error.returncode, error.output) 
	
	return IOLinkedBytecodeFile

def instrumentBytecode(bytecodeFile: Path, dataStatsFile: Path, outputDir: Path) -> Path:

	instrumentedBytecodeFile = outputDir / (bytecodeFile.stem + ".instrumented.bc")
	
	instrumentationCmd = ("opt -load " + RCAPPROX_LLVM_LIB +
							" -profiling -pf " + dataStatsFile.as_posix() +
							" < " + bytecodeFile.as_posix() +
							" > " + instrumentedBytecodeFile.as_posix() + ";")

	linkedBytecodeFile = outputDir / (instrumentedBytecodeFile.stem + ".Linked.bc")

	linkProfileFCallCmd = ("llvm-link -o " + linkedBytecodeFile.as_posix() +
							" " + instrumentedBytecodeFile.as_posix() +
							" " + RCAPPROX_LIB_DIR + "profiler.bc;")
	
	try: 
		subprocess.check_output(instrumentationCmd + linkProfileFCallCmd, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as error:
		raise InstrumentationError(bytecodeFile.as_posix(), error.returncode, error.output)
	
	return linkedBytecodeFile

def executeBytecode(bytecodeFile: Path, inputFile: Path, outputDir: Path) -> Path:

	outputFile = outputDir / (inputFile.stem + ".output.txt")
			
	executionCmd = ("timeout -k 5 " + TIMEOUT +
				    " lli " + bytecodeFile.as_posix() +
				    " " + inputFile.as_posix() +
				    " " + outputFile.as_posix() +
				    " || ! true")
	
	try: 
		subprocess.check_output(executionCmd, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as error:
		raise ExecutionError(bytecodeFile.as_posix(), inputFile.as_posix(), error.returncode, error.output) from error
	
	return outputFile

def variableToConstantTransformation(bytecodeFile: Path, operation: str, constantValue: str, outputDir: Path) -> Path:

    assert (bytecodeFile.is_file() and outputDir.is_dir())

    printMessage('Replacing operation {} of {} by constant value {} ... '.format(operation, bytecodeFile.as_posix(), constantValue), end="", flush=True)
    
    variable2ConstantTransformedBytecodeFile = outputDir / (bytecodeFile.stem + ".pruned_" + operation + ".bc")
    
    variable2ConstantCmd = ("opt -load " + RCAPPROX_LLVM_LIB +
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
    
    optimizeCmd = ("opt -dce -constprop -instcombine -instnamer < " + bytecodeFile.as_posix() +
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

def atoi(text):
    return int(text) if text.isdigit() else text

def naturalKeys(text):
	return [ atoi(c) for c in re.split(r'(\d+)', text[0]) ]

def getAtomRegsFromNetlist(entities: str) -> dict:
	
	regEntities = re.findall("dffeas\s+(.+)\s+\((?:.|\n)*?" + 
								"\.clk\((.*)\),\s+" + 
								"\.d\((.*)\),\s+" + 
								"\.asdata\((.*)\),\s+" + 
								"\.clrn\((.*)\),\s+" + 
								"\.aload\((.*)\),\s+" + 
								"\.sclr\((.*)\),\s+" + 
								"\.sload\((.*)\),\s+" + 
								"\.ena\((.*)\),\s+" + 
								"\.devclrn\((.*)\),\s+" + 
								"\.devpor\((.*)\),\s+" + 
								"\.q\((.*)\),\s+" + 
								"\.prn\((.*)\)\);", entities)

	regs = {}
	for reg in regEntities:
		regName = reg[0]
		regInputs = {reg[2].strip().lstrip('!'), reg[3].strip().lstrip('!'), reg[4].strip().lstrip('!'),
					reg[5].strip().lstrip('!'), reg[6].strip().lstrip('!'), reg[7].strip().lstrip('!'),
					reg[8].strip().lstrip('!')} - {'vcc', 'gnd'} 
		regOutput = reg[11].strip()
		regs[regName] = {'inputs': frozenset(regInputs), 'output': regOutput}

	return regs

def getAtomLutsFromNetlist(entities: str) -> dict:
	
	lutEntities = re.findall("cyclonev_lcell_comb\s+(.+)\s+\((?:.|\n)*?" + 
								"\.dataa\((.*)\),\s+" + 
								"\.datab\((.*)\),\s+" + 
								"\.datac\((.*)\),\s+" + 
								"\.datad\((.*)\),\s+" + 
								"\.datae\((.*)\),\s+" + 
								"\.dataf\((.*)\),\s+" + 
								"\.datag\((.*)\),\s+" + 
								"\.cin\((.*)\),\s+" + 
								"\.sharein\((.*)\),\s+" + 
								"\.combout\((.*)\),\s+" + 
								"\.sumout\((.*)\),\s+" + 
								"\.cout\((.*)\),\s+" + 
								"\.shareout\((.*)\)\);", entities)

	luts = {}
	for lut in lutEntities:
		lutName = lut[0]
		lutInputs = {lut[1].strip().lstrip('!'), lut[2].strip().lstrip('!'), lut[3].strip().lstrip('!'),
					lut[4].strip().lstrip('!'), lut[5].strip().lstrip('!'), lut[6].strip().lstrip('!'),
					lut[7].strip().lstrip('!'), lut[8].strip().lstrip('!'), lut[9].strip().lstrip('!')} - {'vcc', 'gnd'} 
		lutOutputs = {lut[10].strip(), lut[11].strip(), lut[12].strip(), lut[13].strip()} - {''}
		luts[lutName] = {'inputs': frozenset(lutInputs), 'outputs': frozenset(lutOutputs)}

	return luts

def getAtomDspsFromNetlist(entities: str, packedRegs: dict) -> dict:
	
	dspEntities = re.findall("cyclonev_mac\s+(.+)\s+\((?:.|\n)*?" + 
								"\.sub\((.*)\),\s+" + 
								"\.negate\((.*)\),\s+" + 
								"\.accumulate\((.*)\),\s+" + 
								"\.loadconst\((.*)\),\s+" + 
								"\.ax\(((?:.|\n)*?)\),\s+" + 
								"\.ay\(((?:.|\n)*?)\),\s+" + 
								"\.az\(((?:.|\n)*?)\),\s+" + 
								"\.bx\(((?:.|\n)*?)\),\s+" + 
								"\.by\(((?:.|\n)*?)\),\s+" + 
								"\.bz\(((?:.|\n)*?)\),\s+" + 
								"\.coefsela\((.*)\),\s+" + 
								"\.coefselb\((.*)\),\s+" +
								"\.clk\((.*)\),\s+" + 
								"\.aclr\((.*)\),\s+" + 
								"\.ena\((.*)\),\s+" +
								"\.scanin\((.*)\),\s+" + 
								"\.chainin\((.*)\),\s+" +
								"\.dftout\((.*)\),\s+" + 
								"\.resulta\((.*)\),\s+" +
								"\.resultb\((.*)\),\s+" + 
								"\.scanout\((.*)\),\s+" +     
								"\.chainout\((.*)\)\);", entities)

	dsps = {}
	for dsp in dspEntities:
		dspName = dsp[0]
		dspInputs = set(map(lambda each:each.strip().lstrip('!'),
							re.sub('[{}\n]', '', dsp[5]).split(',') +
							re.sub('[{}\n]', '', dsp[6]).split(',') +
							re.sub('[{}\n]', '', dsp[7]).split(',') +
							re.sub('[{}\n]', '', dsp[8]).split(',') +
							re.sub('[{}\n]', '', dsp[9]).split(',') +
							re.sub('[{}\n]', '', dsp[10]).split(','))) - {'vcc', 'gnd'}
		dspOutputs = {reg for reg in packedRegs if packedRegs[reg] == dspName}
		dspOutputs.update({reg for reg in packedRegs if	any(packedRegs[reg] == output and re.sub('\~\d+$', '', dspName) in reg for output in dspOutputs)})
		dsps[dspName] = {'inputs': frozenset(dspInputs), "outputs": frozenset(dspOutputs)} 

	return dsps

def getOpsMetadataFromFile(opsMetadataFile: Path) -> dict:
	
	assert opsMetadataFile.is_file()
	
	operations = dict()

	for line in opsMetadataFile.read_text().splitlines():
		fields = line.split('|')
		operation =re.sub(r'^ID:', '', fields[0])
		operations[operation] = {'type': re.sub(r'^TYPE:', '', fields[1]),
								'signedness': re.sub(r'^SIGN:', '', fields[2]),
								'name': re.sub(r'^NAME:', '', fields[3]), 
								'state': re.sub(r'^STATE:', '', fields[4]),
								'sources': re.sub(r'^SOURCES:', '', fields[5]).split(','),
								'destinations': re.sub(r'^DESTINATIONS:', '', fields[6]).split(','),
								'lutsBytecode': re.sub(r'^LUTs:', '', fields[7]),
								'regsBytecode': re.sub(r'^REGs:', '', fields[8]),
								'dspsBytecode': re.sub(r'^DSPs:', '', fields[9]),
								'lutsNetlist': set(),
								'regsNetlist': set(),
								'dspsNetlist': set()} 
	
	return operations

def getMergedRegsFromFile(mergedRegsRptFile: Path) -> dict:
	
	assert mergedRegsRptFile.is_file()
	
	mergedRegs = dict()
	
	for line in mergedRegsRptFile.read_text().splitlines():
		fields = line.split(':')
		mergedRegs[fields[0]] = fields[1]
		for oldReg, newReg in mergedRegs.items(): 
			if newReg == fields[0]:
				mergedRegs[oldReg] = fields[1]

	return mergedRegs

def getDuplicatedRegsFromFile(duplicatedRegsRptFile: Path) -> dict:
	
	assert duplicatedRegsRptFile.is_file()
	
	duplicatedRegs = dict()
	
	for line in duplicatedRegsRptFile.read_text().splitlines():
		fields = line.split(':')
		duplicatedRegs[fields[0]] = fields[1] 
	
	return duplicatedRegs

def getRemovedRegsFromFile(removedRegsRptFile: Path) -> set:
	
	assert removedRegsRptFile.is_file()
	
	removedRegs = set()
	
	for reg in removedRegsRptFile.read_text().splitlines():
		removedRegs.add(reg) 
	
	return removedRegs

def getPackedRegsFromFile(packedRegsRptFile: Path) -> dict:
	
	assert packedRegsRptFile.is_file()
	
	packedRegs = dict()
	
	for line in packedRegsRptFile.read_text().splitlines():
		fields = line.split(':')
		packedRegs[fields[0]] = fields[1] 
	
	return packedRegs

def removeLogicConstantOps(operations: dict) -> dict:
	
	logicOps = {'shl', 'lshr', 'ashr', 'and', 'or', 'xor'}
	
	removedOps = dict()
	
	for operation, metadata in sorted(operations.items(), key=naturalKeys):
	
		numDestinationsSameState = 0
		numDestinations = len(metadata['destinations'])
		numSources = len(metadata['sources'])
		operationType = metadata['type']
		destinations = metadata['destinations']
		sources = metadata['sources']
		state = metadata['state']
	
		if operationType in logicOps and numSources == 1:
			for destination in destinations:
				if destination in operations and operations[destination]['state'] == state and operations[destination]['type'] != 'phi':
	
					operations[destination]['sources'].remove(operation)
					operations[destination]['sources'].append(sources[0])
					numDestinationsSameState += 1
	
			if numDestinationsSameState == numDestinations:
				removedOps[operation] = operations.pop(operation)
	
	return removedOps

def getQuartusOperatorLuts(lutAtoms: dict) -> dict:
	
	operatorLuts = dict()
	
	for lut in lutAtoms:
		match = re.match("^((?:(?!lpm_mult).)+\|" +
						"(?:Add|Mult|Div|Equal|ShiftLeft|" + 
						"ShiftRight|Mod|LessThan|Mux|Selector|" +
						"Decoder|always)\d+)\~\d+$", lut) 
		if match:
			operatorLut = match.group(1)
			if operatorLut not in operatorLuts:
				operatorLuts[operatorLut] = {lut}
			else:
				operatorLuts[operatorLut].add(lut)

	return operatorLuts

def  updateResourcesFromAtoms(operations: dict, mergedRegs: dict, duplicatedRegs: dict,
                            removedRegs: set, packedRegs: dict, atomLuts: dict,
                            atomRegs: dict, atomDsps: dict):

	for operation, metadata in operations.items():
		
		name = metadata['name'] 
		luts = {lutName for lutName in atomLuts if name in lutName}
		
		regs = {regName for regName in atomRegs if name in regName}
		
		opMergedRegs = {mergedRegs[regName] for regName in mergedRegs if
								name in regName and mergedRegs[regName] not in removedRegs}
		
		opMergedAndDuplicatedRegs = {duplicatedRegs[regName] for regName in duplicatedRegs if
											any(reg in regName for reg in opMergedRegs)}
		
		opMergedRegs.update(opMergedAndDuplicatedRegs)
		
		opPackedRegs = {regName: packedRegs[regName] for regName in packedRegs if
								any(reg in regName for reg in opMergedRegs.union({name}))}
		
		regs.update(opMergedRegs.difference(set(opPackedRegs.keys()))) 
		
		dsps = {dspName for dspName in atomDsps if name in dspName}
		
		metadata['lutsNetlist'].update(luts)
		metadata['regsNetlist'].update(regs)
		metadata['dspsNetlist'].update(dsps)

	removedOps = removeLogicConstantOps(operations)
	
	operatorLuts = getQuartusOperatorLuts(atomLuts)
	jaccardSimilarity = {}
	for operator, luts in sorted(operatorLuts.items(), key=naturalKeys):
		
		operatorInputs = set(itertools.chain.from_iterable([atomLuts[lut]['inputs'] for lut in luts]))
		operatorOutputs = set(itertools.chain.from_iterable([atomLuts[lut]['outputs'] for lut in luts]))
		operatorInternals = operatorInputs.intersection(operatorOutputs)
		operatorInputs.difference_update(operatorInternals)
		operatorOutputs.difference_update(operatorInternals)

		for operation, metadata in operations.items():

			sourcesRegsOutputs = [] 
			sourcesLutsOutputs = []
			sourcesDspsOutputs = []
			for source in metadata['sources']:
				if source in operations: 
					if operations[source]['state'] == metadata['state'] and operations[source]['type'] != 'phi':
						sourceLutsInputs = set(itertools.chain.from_iterable([atomLuts[lut]['inputs'] for lut in operations[source]['lutsNetlist']]))
						sourceLutsOutputs = set(itertools.chain.from_iterable([atomLuts[lut]['outputs'] for lut in operations[source]['lutsNetlist']]))
						sourceDspsInputs = set(itertools.chain.from_iterable([atomDsps[dsp]['inputs'] for dsp in operations[source]['dspsNetlist']]))
						sourceDspsOutputs = set(itertools.chain.from_iterable([atomDsps[dsp]['outputs'] for dsp in operations[source]['dspsNetlist']]))
												
						sourceLutsInternals = sourceLutsOutputs.intersection(sourceLutsInputs.union(sourceDspsInputs))
						sourceDspsInternals = sourceDspsOutputs.intersection(sourceDspsInputs.union(sourceLutsInputs)) 
						sourceLutsOutputs.difference_update(sourceLutsInternals)
						sourceDspsOutputs.difference_update(sourceDspsInternals)

						sourcesLutsOutputs.append(sourceLutsOutputs)
						sourcesDspsOutputs.append(sourceDspsOutputs)
						
					else:
						sourceRegsOutputs = set(map(lambda each:atomRegs[each]['output'], operations[source]['regsNetlist']))
						sourcesRegsOutputs.append(sourceRegsOutputs)

			regsInputs = [set(itertools.chain.from_iterable([atomRegs[reg]['inputs'] for reg in metadata['regsNetlist']]))]
			destinationsLutsInputs = []
			destinationsDspsInputs = []
			destinationsRegsInputs = []
			for destination in metadata['destinations']:
				if destination in operations: 
					if operations[destination]['state'] == metadata['state'] and operations[destination]['type'] != 'phi':
						destinationLutsInputs = set(itertools.chain.from_iterable([atomLuts[lut]['inputs'] for lut in operations[destination]['lutsNetlist']]))
						destinationLutsOutputs = set(itertools.chain.from_iterable([atomLuts[lut]['outputs'] for lut in operations[destination]['lutsNetlist']]))
						destinationDspsInputs = set(itertools.chain.from_iterable([atomDsps[dsp]['inputs'] for dsp in operations[destination]['dspsNetlist']]))
						destinationDspsOutputs = set(itertools.chain.from_iterable([atomDsps[dsp]['outputs'] for dsp in operations[destination]['dspsNetlist']]))
						destinationRegsInputs = set(itertools.chain.from_iterable([atomRegs[reg]['inputs'] for reg in operations[destination]['regsNetlist']]))
						
						destinationLutsInternals = destinationLutsInputs.intersection(destinationLutsOutputs.union(destinationDspsOutputs))
						destinationDspsInternals = destinationDspsInputs.intersection(destinationDspsOutputs.union(destinationLutsOutputs)) 
						destinationLutsInputs.difference_update(destinationLutsInternals)
						destinationDspsInputs.difference_update(destinationDspsInternals)

						destinationsLutsInputs.append(destinationLutsInputs)
						destinationsDspsInputs.append(destinationDspsInputs)
						destinationsRegsInputs.append(destinationRegsInputs)
				
			sourcesOutputs = filter(None, sourcesRegsOutputs + sourcesLutsOutputs + sourcesDspsOutputs)
			destinationsInputs = filter(None, destinationsRegsInputs + destinationsLutsInputs + destinationsDspsInputs + regsInputs)
			
			matchInputs = operatorInputs.issubset(set().union(*sourcesOutputs)) and not any(operatorInputs.isdisjoint(sourceOutput) for sourceOutput in sourcesOutputs) 
			matchOutputs = operatorOutputs.issubset(set().union(*destinationsInputs)) and not any(operatorOutputs.isdisjoint(destinationInput) for destinationInput in destinationsInputs) 
						
			inputsJaccardSimilarity = len(operatorInputs.intersection(set().union(*sourcesOutputs))) / len(operatorInputs.union(set().union(*sourcesOutputs)))
			outputsJaccardSimilarity = len(operatorOutputs.intersection(set().union(*destinationsInputs))) / len(operatorOutputs.union(set().union(*destinationsInputs)))
			
			if inputsJaccardSimilarity > 0 or outputsJaccardSimilarity > 0: 
				if operator not in jaccardSimilarity:
					jaccardSimilarity[operator] = {operation: (inputsJaccardSimilarity + outputsJaccardSimilarity) / 2}
				else:
					jaccardSimilarity[operator][operation] = (inputsJaccardSimilarity + outputsJaccardSimilarity) / 2 

		if operator in jaccardSimilarity: 
			candidates = jaccardSimilarity[operator] 
			selectedCandidate = max(candidates, key=lambda key: candidates[key])
			operations[selectedCandidate]['lutsNetlist'].update(luts)
	

def updateOpsMetadataFromNetlist(opsMetadataFile: Path, mergedRegsRptFile: Path, duplicatedRegsRptFile: Path,
                                removedRegsRptFile: Path, packedRegsRptFile: Path, quartusNetlistRptFile: Path) -> dict:

	assert (opsMetadataFile.is_file() and mergedRegsRptFile.is_file() and duplicatedRegsRptFile.is_file()
			and removedRegsRptFile.is_file() and packedRegsRptFile.is_file() and quartusNetlistRptFile.is_file())
	
	printMessage('Updating operations metadata in {} with compilation results ... '.format(opsMetadataFile.as_posix()), end="", flush=True)

	operations = getOpsMetadataFromFile(opsMetadataFile)
	
	mergedRegs = getMergedRegsFromFile(mergedRegsRptFile)
	duplicatedRegs = getDuplicatedRegsFromFile(duplicatedRegsRptFile)
	removedRegs = getRemovedRegsFromFile(removedRegsRptFile)
	packedRegs = getPackedRegsFromFile(packedRegsRptFile)

	quartusAtomEntities = quartusNetlistRptFile.read_text()
	atomLuts = getAtomLutsFromNetlist(quartusAtomEntities)
	atomRegs = getAtomRegsFromNetlist(quartusAtomEntities)
	atomDsps = getAtomDspsFromNetlist(quartusAtomEntities, packedRegs)

	updateResourcesFromAtoms(operations, mergedRegs, duplicatedRegs, removedRegs, packedRegs, atomLuts, atomRegs, atomDsps)
	
	printMessage('Done!')

	return operations

def getPercentageVariationStr(baseValue: int, newValue: int) -> str:
	
	assert baseValue >= 0 and newValue >=0

	if baseValue == newValue:
		return '0%' 
	elif baseValue == 0: 
		return 'n/a'
	else:
		return '{:+.2f}'.format(((newValue - baseValue) / baseValue)*100).rstrip('0') + '%'
		
def estimateResourcesSavings(parentDesignOpsMetadata: dict,
							 approxDesignOpsMetadata: dict) -> (int, int, int):

	LUTsSaved = 0
	REGsSaved = 0
	DSPsSaved = 0

	for operation in parentDesignOpsMetadata:
		if operation not in approxDesignOpsMetadata:
			
			LUTsSaved += len(parentDesignOpsMetadata[operation]['lutsNetlist'])
			REGsSaved += len(parentDesignOpsMetadata[operation]['regsNetlist'])
			DSPsSaved += len(parentDesignOpsMetadata[operation]['dspsNetlist'])
				
		else:
			LUTsSaved += (len(parentDesignOpsMetadata[operation]['lutsNetlist']) - len(approxDesignOpsMetadata[operation]['lutsNetlist'])) 
			REGsSaved += (len(parentDesignOpsMetadata[operation]['regsNetlist']) - len(approxDesignOpsMetadata[operation]['regsNetlist']))
			DSPsSaved += (len(parentDesignOpsMetadata[operation]['dspsNetlist']) - len(approxDesignOpsMetadata[operation]['dspsNetlist']))
					
	for op in approxDesignOpsMetadata:
		if op not in parentDesignOpsMetadata:

			LUTsSaved -= len(approxDesignOpsMetadata[op]['lutsNetlist'])
			REGsSaved -= len(approxDesignOpsMetadata[op]['regsNetlist'])
			DSPsSaved -= len(approxDesignOpsMetadata[op]['dspsNetlist'])
	
	return LUTsSaved, REGsSaved, DSPsSaved

def getFitness(LUTsToSave: int, LUTsSaved: int,
				REGsToSave: int, REGsSaved: int,
				DSPsToSave: int, DSPsSaved: int,
				mseValue: float) -> float:

	resourceTypes = 0
	relativeLUTsSaved = 0
	relativeREGsSaved = 0
	relativeDSPsSaved = 0

	if LUTsToSave > 0: 
		relativeLUTsSaved = numpy.clip(LUTsSaved / LUTsToSave, 0, 1)
		resourceTypes += 1

	if REGsToSave > 0:
		relativeREGsSaved  = numpy.clip(REGsSaved / REGsToSave, 0, 1)
		resourceTypes += 1

	if DSPsToSave > 0:
		relativeDSPsSaved = numpy.clip(DSPsSaved / DSPsToSave, 0, 1)
		resourceTypes += 1
	
	assert resourceTypes > 0
	
	relativeResourcesSavings = (relativeLUTsSaved + relativeREGsSaved + relativeDSPsSaved) / resourceTypes
		
	if mseValue == 0:
		return relativeResourcesSavings
	else:
		return relativeResourcesSavings / mseValue 

def selectBestFitApproxDesigns(approxDesigns: dict) -> dict:
	
	for	approxDesignBytecodeFile1, approxDesignBytecodeFile2 in itertools.permutations(approxDesigns, 2):
			if (approxDesignBytecodeFile1 in approxDesigns
				and approxDesignBytecodeFile2 in approxDesigns 
				and approxDesigns[approxDesignBytecodeFile1]['LUTsToSave'] >= approxDesigns[approxDesignBytecodeFile2]['LUTsToSave']
				and approxDesigns[approxDesignBytecodeFile1]['REGsToSave'] >= approxDesigns[approxDesignBytecodeFile2]['REGsToSave']
				and approxDesigns[approxDesignBytecodeFile1]['DSPsToSave'] >= approxDesigns[approxDesignBytecodeFile2]['DSPsToSave']
				and approxDesigns[approxDesignBytecodeFile1]['mse'] >= approxDesigns[approxDesignBytecodeFile2]['mse']):
				del approxDesigns[approxDesignBytecodeFile1]	
		
	return dict(sorted(approxDesigns.items(), key=lambda kv: kv[1]['fitness'], reverse=True)[:MAX_BRANCHES])

def genApproxDesigns(parentDesignBytecodeFile: Path, parentDesignOpsMetadata: dict,
							parentDesignReportFiles: dict, trainingDataProfile: dict,
                            parentLUTs: int, parentREGs: int, parentDSPs: int,
							LUTsToSave: int, REGsToSave: int, DSPsToSave: int,
							goldenOutputsTraining: dict, trainingInputsDir: Path, outputsDir: Path) -> (Path, dict):

	approxDesigns = dict()
	
	for operation in (parentDesignOpsMetadata.keys() & trainingDataProfile.keys()):

		approxOpDir = outputsDir / ("op_" + operation)
		approxOpDir.mkdir()

		approxOpTrainingOutputsDir = approxOpDir / "outputs/training"
		approxOpTrainingOutputsDir.mkdir(parents=True)
				
		grandMean = float(trainingDataProfile[operation]['grandMean'])
		grandStdDev = float(trainingDataProfile[operation]['grandStdDev'])
		bitwidth = int(trainingDataProfile[operation]['bitwidth'])

		constantValue = str(getConstantValueFromStatistics(grandMean, grandStdDev, bitwidth))

		try:
			approxDesignBytecodeFile = variableToConstantTransformation(parentDesignBytecodeFile, operation, constantValue, approxOpDir)
			approxDesignOptimizedBytecodeFile = optimizeBytecode(approxDesignBytecodeFile, approxOpDir)
			approxDesignUpdatedBytecodeFile = updateBytecodeOpsMetadata(approxDesignOptimizedBytecodeFile, approxOpDir)
			approxDesignOpsMetadataFile = getOpsMetadataFromBytecode(approxDesignUpdatedBytecodeFile, parentDesignReportFiles['scheduling'], approxOpDir) 
			approxDesignOutputsValues = getOutputsValues(approxDesignUpdatedBytecodeFile, trainingInputsDir, approxOpTrainingOutputsDir, deleteOutputFiles=True)
			approxDesignMseValues = getMseValues(approxDesignOutputsValues, goldenOutputsTraining)
		except ExecutionError as error: 
			print('Info: execution of {} returned error code {}. Operation {} cannot be approximated.'.format(error.bytecode, error.errorCode, operation))
			continue
		except RCApproxException: raise
		
		approxDesignOpsMetadata = updateOpsMetadataFromNetlist(approxDesignOpsMetadataFile,
																parentDesignReportFiles['mergedRegs'],
																parentDesignReportFiles['duplicatedRegs'],
																parentDesignReportFiles['removedRegs'],
																parentDesignReportFiles['packedRegs'],
																parentDesignReportFiles['netlist'])
		
		LUTsSaved, REGsSaved, DSPsSaved = estimateResourcesSavings(parentDesignOpsMetadata, approxDesignOpsMetadata)
		meanMseValue = numpy.mean(list(approxDesignMseValues.values()), dtype=numpy.float64)
		meanStdDevValue = numpy.std(list(approxDesignMseValues.values()), dtype=numpy.float64)
		meanPsnrValue = (20 * numpy.log10((2**OUTPUT_BITWIDTH - 1) / numpy.sqrt(meanMseValue, dtype=numpy.float64), dtype=numpy.float64)
					if meanMseValue > 0 else numpy.inf)
		fitness = getFitness(LUTsToSave, LUTsSaved, REGsToSave, REGsSaved, DSPsToSave, DSPsSaved, meanMseValue)	
		
		optimizationLogFile = approxOpDir / (approxDesignUpdatedBytecodeFile.stem + ".optimizations.txt")
		optimizationLogFile.write_text('Oeration Approximated: ID:{}|TYPE:{}|NAME:{}|STATE:{}|LUTs:{}|REGs:{}|DSPs:{}\n'
										'Constant Substitution: {}\n' 
										'Estimated LUTs savings: {}\n' 
										'Estimated REGs savings: {}\n' 
										'Estimated DSPs savings: {}\n' 
										'Mean MSE: {:.2f}\n'
										'MSE Std Dev: {:.2f}\n'
										'Mean PSNR: {:.2f}\n' 
										'Fitness: {}'.format(
										operation,
										parentDesignOpsMetadata[operation]['type'],
										parentDesignOpsMetadata[operation]['name'],
										parentDesignOpsMetadata[operation]['state'],
										len(parentDesignOpsMetadata[operation]['lutsNetlist']),
										len(parentDesignOpsMetadata[operation]['regsNetlist']),
										len(parentDesignOpsMetadata[operation]['dspsNetlist']),
										constantValue, LUTsSaved, REGsSaved,
										DSPsSaved, meanMseValue, meanStdDevValue, meanPsnrValue, fitness))

		approxDesigns[approxDesignUpdatedBytecodeFile] = {'fitness': fitness,
															'mse': meanMseValue,
															'stdDev': meanStdDevValue,
															'psnr': meanPsnrValue, 
															'ops': approxDesignOpsMetadataFile,
															'opts': optimizationLogFile,
                                                            'parentLUTs': parentLUTs,
                                                            'parentREGs': parentREGs,
                                                            'parentDSPs': parentDSPs,
															'LUTsSaved': LUTsSaved,
															'REGsSaved': REGsSaved,
															'DSPsSaved': DSPsSaved,
															'LUTsToSave': max(0, LUTsToSave - LUTsSaved),
															'REGsToSave': max(0, REGsToSave - REGsSaved),
															'DSPsToSave': max(0, DSPsToSave - DSPsSaved)}
	return approxDesigns