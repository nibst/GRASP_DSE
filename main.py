from ast import arguments
from pickle import TRUE

from setuptools import Require
from greedy import Greedy
from hillClimbing0 import HillClimbing
import argparse



if __name__ == "__main__":
    

 
    #Initialize parser
    parser = argparse.ArgumentParser()
 
    # Adding argument
    parser.add_argument("-c", "--cFiles", help = "C input files list", required=TRUE, nargs='+')
    parser.add_argument("-d", "--dFile", help = "Directives input file",required=TRUE)
    parser.add_argument("-p", "--prjFile", help = "Prj. top file",required=TRUE)

 
    # Read arguments from command line
    args = parser.parse_args()
    
    filesDict = {}
    filesDict['cFiles'] = args.cFiles
    filesDict['dFile'] = args.dFile
    filesDict['prjFile'] = args.prjFile
    

    
    shaHill0 = HillClimbing(filesDict,'directives.tcl')
    shaHill0.writeSolutionsDict()
   
