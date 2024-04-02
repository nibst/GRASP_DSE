from os import environ
from pathlib2 import Path
from lib.rcapproxlib import *
import argparse
import numpy
import itertools
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument('EXACT_DESIGN_BC', type=str, nargs=1)
parser.add_argument('MAX_LUTS', type=int, nargs=1)
parser.add_argument('MAX_REGS', type=int, nargs=1)
parser.add_argument('MAX_DSPS', type=int, nargs=1)
parsed = parser.parse_args() 

EXACT_DESIGN_BC = parsed.EXACT_DESIGN_BC[0]
MAX_LUTS = parsed.MAX_LUTS[0]
MAX_REGS = parsed.MAX_REGS[0]
MAX_DSPS = parsed.MAX_DSPS[0]

try:
	DESIGN_NAME = environ['NAME']
	TRAINING_VECS_DIR = environ['TRAINING_VECS_DIR']
	TEST_VECS_DIR = environ['TEST_VECS_DIR']
	OUTPUT_BITWIDTH = int(environ['OUTPUT_BITWIDTH'])
except KeyError as error:
	print('Error: environment variable {} not defined.'.format(error.args[0]))
	raise

resultsDir = Path("rcapprox_results")
resultsDir.mkdir()
exactDesignDir = resultsDir / "exact_design"
exactDesignDir.mkdir()
exactDesignProfilesDir = exactDesignDir / "profiles"
exactDesignProfilesDir.mkdir()
exactDesignOutputsDir = exactDesignDir / "outputs"
exactDesignOutputsDir.mkdir()
exactDesignTestOutputsDir = exactDesignOutputsDir / "test"
exactDesignTestOutputsDir.mkdir()
exactDesignTrainingOutputsDir = exactDesignOutputsDir / "training"
exactDesignTrainingOutputsDir.mkdir()
approxDesignsDir = resultsDir / "approx_designs"
approxDesignsDir.mkdir()
finalDesignDir = resultsDir / "final_design"
finalDesignDir.mkdir()
finalDesignOutputsDir = finalDesignDir / "outputs"
finalDesignOutputsDir.mkdir()
finalDesignTestOutputsDir = finalDesignOutputsDir / "test"
finalDesignTestOutputsDir.mkdir()
trainingInputsDir = Path(TRAINING_VECS_DIR)
testInputsDir = Path(TEST_VECS_DIR)

def main():
	
	print('Info: the resource constrained approximation heuristic has started (Max LUTs: {}, Max REGs: {}, Max DSPs: {})'.format(MAX_LUTS, MAX_REGS, MAX_DSPS))
	print ('Info: compiling the exact design ...')
	exactDesignBytecodeFile = exactDesignDir / EXACT_DESIGN_BC
	Path(EXACT_DESIGN_BC).replace(exactDesignBytecodeFile)
	
	# evaluate actual resources usage of exact design (LUTs, REGs and DSPs) and get operations metadata
	try:
		exactDesignUpdatedBytecodeFile = updateBytecodeOpsMetadata(exactDesignBytecodeFile, exactDesignDir)
		exactDesignReportFiles = compileBytecode(exactDesignUpdatedBytecodeFile, exactDesignDir)
		exactDesignOpsMetadataFile = getOpsMetadataFromBytecode(exactDesignUpdatedBytecodeFile, exactDesignReportFiles['scheduling'], exactDesignDir)
		goldenOutputsTest = getOutputsValues(exactDesignUpdatedBytecodeFile, testInputsDir, exactDesignTestOutputsDir, deleteOutputFiles=False)
		goldenOutputsTraining, dataStatsTraining = getOutputsValuesAndDataStats(exactDesignUpdatedBytecodeFile,
																				trainingInputsDir,
																				exactDesignTrainingOutputsDir,
																				exactDesignProfilesDir, deleteOutputFiles=False)
		
		exactDesignLUTs, exactDesignREGs, exactDesignDSPs = getDesignResourcesFromFile(exactDesignReportFiles['resources'])
	except RCApproxException:
		print("Error: something went wrong when trying to profile the exact design.")
		raise
	
	# set the number of resources to save for each resource type 	
	LUTsToSave = exactDesignLUTs - MAX_LUTS
	REGsToSave = exactDesignREGs - MAX_REGS
	DSPsToSave = exactDesignDSPs - MAX_DSPS

	print('Info: exact design uses {} LUTs, {} REGs, and {} DSPs'.format(exactDesignLUTs, exactDesignREGs, exactDesignDSPs))

	# set the exact design as the parent design for the first iteration
	parentDesigns = dict()
	if LUTsToSave > 0 or REGsToSave > 0 or DSPsToSave > 0:
		parentDesigns[exactDesignUpdatedBytecodeFile] = {'opsMetadataFile': exactDesignOpsMetadataFile,
														'reportFiles': exactDesignReportFiles,
														'LUTs': exactDesignLUTs,
														'REGs': exactDesignREGs,
														'DSPs': exactDesignDSPs,
														'LUTsToSave': LUTsToSave,
														'REGsToSave': REGsToSave,
														'DSPsToSave': DSPsToSave,
														'psnr': 'inf'}
	else:
		print('Info: exact design already meets all resources contraints.')
		exit(0)
	
	# iterative design space exploration (greedy)
	functionArgs = list()
	approxDesigns = dict()
	finalDesigns = dict()
	iteration = 1
	while len(parentDesigns) > 0:
		
		iterationDir = approxDesignsDir / ("iteration_" + str(iteration))
		iterationDir.mkdir()

		print('Info: iteration {} has started. Trere is/are {} parent(s) to explore ...'.format(iteration, len(parentDesigns)))

		for idx, (parentDesignBytecodeFile, parentDesignProfile) in enumerate(parentDesigns.items()):

			print('Parent {} -> LUTs to save: {}, REGs to save: {}, DSPs to save: {}, PSNR: {}'.format(idx + 1, parentDesignProfile['LUTsToSave'], parentDesignProfile['REGsToSave'], parentDesignProfile['DSPsToSave'], parentDesignProfile['psnr']))

			parentDir = iterationDir / ("parent_" + str(idx + 1))
			parentDir.mkdir()

			parentDesignOpsMetadata = updateOpsMetadataFromNetlist(parentDesignProfile['opsMetadataFile'],
																	parentDesignProfile['reportFiles']['mergedRegs'],
																	parentDesignProfile['reportFiles']['duplicatedRegs'],
																	parentDesignProfile['reportFiles']['removedRegs'],
																	parentDesignProfile['reportFiles']['packedRegs'],
																	parentDesignProfile['reportFiles']['netlist'])

			functionArgs.append((parentDesignBytecodeFile, parentDesignOpsMetadata,
								parentDesignProfile['reportFiles'], dataStatsTraining,
								parentDesignProfile['LUTs'], parentDesignProfile['REGs'], parentDesignProfile['DSPs'],
								parentDesignProfile['LUTsToSave'], parentDesignProfile['REGsToSave'], parentDesignProfile['DSPsToSave'], goldenOutputsTraining,
								trainingInputsDir, parentDir))
			
		# generating dict of approx designs
		print('Info: explorirng parent(s) design(s) ...')
		with ThreadPoolExecutor(max_workers = len(functionArgs)) as executor:
			results = executor.map(lambda p: genApproxDesigns(*p), functionArgs)
		for result in results:
			approxDesigns.update(result)

		# select Pareto-optimal designs relative to error and how many resources of each type are still left to eliminate
		bestFitApproxDesigns = selectBestFitApproxDesigns(approxDesigns)
		
		# evaluate and save actual resources usage (LUTs, REGs and DSPs) and metadata of selected designs
		selectedDesignsDir = iterationDir / "selected_designs"
		selectedDesignsDir.mkdir()
		selectedDesignsLogFile = approxDesignsDir / ("iteration_" + str(iteration) + ".log.txt") 
		logText = ''
		parentDesigns.clear()
		
		for idx, (approxDesignBytecodeFile, approxDesignProfile) in enumerate(bestFitApproxDesigns.items()):
				
			selectedDesignBytecodeFile = selectedDesignsDir / (DESIGN_NAME + '.' + str(idx + 1) + '.bc')
			approxDesignBytecodeFile.replace(selectedDesignBytecodeFile)
			
			selectedDesignReportFiles = compileBytecode(selectedDesignBytecodeFile, selectedDesignsDir)
			selectedDesignOpsMetadataFile = getOpsMetadataFromBytecode(selectedDesignBytecodeFile, selectedDesignReportFiles['scheduling'], selectedDesignsDir) 
			selectedDesignLUTs, selectedDesignREGs, selectedDesignDSPs = getDesignResourcesFromFile(selectedDesignReportFiles['resources'])
			
			# save iteration result
			logText += ('Approximated Design: {}\n'
						'LUTs: {} ({})\n' 
						'REGs: {} ({})\n' 
						'DSPs: {} ({})\n\n' 
						'Actual LUT Savings: {}\n' 
						'Actual REG Savings: {}\n' 
						'Actual DSP Savings: {}\n\n' 
						'Estimated LUT Savings: {}\n' 
						'Estimated REG Savings: {}\n' 
						'Estimated DSP Savings: {}\n\n' 
						'Mean MSE (training): {:.2f}\n'
						'MSE Std Dev: {:.2f}\n'
						'Mean PSNR (training): {:.2f}\n\n'.format(
						selectedDesignBytecodeFile,
						selectedDesignLUTs,
						getPercentageVariationStr(exactDesignLUTs, selectedDesignLUTs),
						selectedDesignREGs,
						getPercentageVariationStr(exactDesignREGs, selectedDesignREGs),
						selectedDesignDSPs,
						getPercentageVariationStr(exactDesignDSPs, selectedDesignDSPs),
						approxDesignProfile['parentLUTs'] - selectedDesignLUTs,
						approxDesignProfile['parentREGs'] - selectedDesignREGs,
						approxDesignProfile['parentDSPs'] - selectedDesignDSPs,
						approxDesignProfile['LUTsSaved'],
						approxDesignProfile['REGsSaved'],
						approxDesignProfile['DSPsSaved'],
						approxDesignProfile['mse'],
						approxDesignProfile['stdDev'],
						approxDesignProfile['psnr']))
			
			if selectedDesignLUTs <= MAX_LUTS and selectedDesignREGs <= MAX_REGS and selectedDesignDSPs <= MAX_DSPS:
				finalDesigns[selectedDesignBytecodeFile] = {'opsMetadataFile': selectedDesignOpsMetadataFile,
															'reportFiles': selectedDesignReportFiles,
															'LUTs': selectedDesignLUTs,
															'REGs': selectedDesignREGs,
															'DSPs': selectedDesignDSPs,
															'mse': approxDesignProfile['mse'],
															'psnr': approxDesignProfile['psnr']}    
			elif all(approxDesignProfile['mse'] < finalDesigns[finalDesign]['mse'] for finalDesign in finalDesigns):
				parentDesigns[selectedDesignBytecodeFile] = {'opsMetadataFile': selectedDesignOpsMetadataFile,
															'reportFiles': selectedDesignReportFiles,
															'LUTs': selectedDesignLUTs,
															'REGs': selectedDesignREGs,
															'DSPs': selectedDesignDSPs,
															'LUTsToSave': selectedDesignLUTs - MAX_LUTS,
															'REGsToSave': selectedDesignREGs - MAX_REGS,
															'DSPsToSave': selectedDesignDSPs - MAX_DSPS,
															'mse': approxDesignProfile['mse'],
															'psnr': approxDesignProfile['psnr']}
		selectedDesignsLogFile.write_text(logText) 
		del functionArgs[:]
		approxDesigns.clear()		
		iteration += 1

	# constraints are met, save final design (.bc, .v, and metadata)
	if len(finalDesigns) == 0:
		print("Info: constraints cannot be met: there are no enough arithmetic or logic operations to approximate.")
		exit(0)

	finalDesign = min(finalDesigns, key=lambda key: finalDesigns[key]['mse'])
	finalDesignVerilog = finalDesigns[finalDesign]['reportFiles']['verilog']
	finalDesignOpsMetadata = finalDesigns[finalDesign]['opsMetadataFile']

	finalDesignBytecodeFile = finalDesignDir / (DESIGN_NAME + ".bc")
	finalDesign.replace(finalDesignBytecodeFile)
	
	finalDesignVerilogFile = finalDesignDir / (DESIGN_NAME + ".v")
	finalDesignVerilog.replace(finalDesignVerilogFile)
	
	finalDesignOpsMetadataFile = finalDesignDir / (DESIGN_NAME + ".metadata.txt")
	finalDesignOpsMetadata.replace(finalDesignOpsMetadataFile)
	
	# evaluate mean MSE of final design with test vectors
	try:
		finalDesignOutputsValues = getOutputsValues(finalDesignBytecodeFile, testInputsDir, finalDesignTestOutputsDir) 
		finalDesignMseValues = getMseValues(finalDesignOutputsValues, goldenOutputsTest)
		meanFinalDesignMseValue = numpy.mean(list(finalDesignMseValues.values()), dtype=numpy.float64)
		meanFinalDesignStdDevValue = numpy.std(list(finalDesignMseValues.values()), dtype=numpy.float64)
		meanFinalDesignPsnrValue = (20 * numpy.log10((2**OUTPUT_BITWIDTH - 1) / numpy.sqrt(meanFinalDesignMseValue, dtype=numpy.float64), dtype=numpy.float64)
					if meanFinalDesignMseValue > 0 else numpy.inf)
	except RCApproxException:
		print("Error: something went wrong when trying to evaluate the final design error.")
		raise
	
	# save final result (actual resources usage, MSE, Std Dev, and PSNR)
	finalDesignLogFile = finalDesignDir / "finalDesignMetrics.txt"
	finalDesignLogFile.write_text('LUTs: {}\nREGs: {}\nDSPs: {}\nMean MSE (test): {:.2f}\nMSE Std Dev: {:.2f}\nMean PSNR (test): {:.2f}'.format(
									finalDesigns[finalDesign]['LUTs'],
									finalDesigns[finalDesign]['REGs'],
									finalDesigns[finalDesign]['DSPs'],
									meanFinalDesignMseValue,
									meanFinalDesignStdDevValue,
									meanFinalDesignPsnrValue))
	
	print('Info: constraints met! the final design can be found in {}'.format(finalDesignDir.as_posix()))
	exit(0)	

if __name__ == '__main__':
	main()
