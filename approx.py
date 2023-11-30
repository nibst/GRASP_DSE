from os import environ
from pathlib2 import Path
from lib.approxLib import *
import argparse
from concurrent.futures import ThreadPoolExecutor
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

"""
approx_results/
|
--+approx_design/
--+exact_design/
  |
  --+profiles/
  --+outputs/
    |
    --+test/
    --+training/
"""
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

def main():
	
	print ('Info: compiling the exact design ...')
	exactDesignBytecodeFile = exactDesignDir / EXACT_DESIGN_BC
	shutil.copy(EXACT_DESIGN_BC,exactDesignBytecodeFile)
	
	# evaluate actual resources usage of exact design (LUTs, REGs and DSPs) and get operations metadata
	try:
		exactDesignUpdatedBytecodeFile = updateBytecodeOpsMetadata(exactDesignBytecodeFile, exactDesignDir)
		#exactDesignReportFiles = compileBytecode(exactDesignUpdatedBytecodeFile, exactDesignDir)
		#exactDesignOpsMetadataFile = getOpsMetadataFromBytecode(exactDesignUpdatedBytecodeFile, exactDesignReportFiles['scheduling'], exactDesignDir)
		
		
		goldenOutputsTest = getOutputsValues(exactDesignUpdatedBytecodeFile, testInputsDir, exactDesignTestOutputsDir, deleteOutputFiles=False)
		goldenOutputsTraining, dataStatsTraining = getOutputsValuesAndDataStats(exactDesignUpdatedBytecodeFile,
																				trainingInputsDir,
																				exactDesignTrainingOutputsDir,
																				exactDesignProfilesDir, deleteOutputFiles=False)
		
		#exactDesignLUTs, exactDesignREGs, exactDesignDSPs = getDesignResourcesFromFile(exactDesignReportFiles['resources'])
		print("OK")
	except RCApproxException:
		print("Error: something went wrong when trying to profile the exact design.")
		raise
	finally:
		shutil.rmtree('./approx_results')
if __name__ == '__main__':
	main()
