from ast import arguments
from pickle import TRUE

from setuptools import Require
from greedy import Greedy
from hillClimbing0 import HillClimbing
import sys, os, subprocess, argparse



if __name__ == "__main__":
    #subprocess.call([r'C:\Xilinx\Vivado\2020.2\settings64.bat'])
    #benchmark = sys.argv[1]
    #output = sys.argv[2]
    #result = HillClimbing(benchmark,output)
    #result.writeSolutions()
    #os.system('vivado')
    #os.system('vivado -mode batch -source run_hls.tcl')
    # argumentsList = sys.argv[1:]
    # # Options
    # # Long options
    # options = ["-c", "-d", "-p", "-cFile", "-prjFile","-dirFile"]
    
    # for argumentOrValue in argumentsList:
    #     if argumentOrValue in ["-c", "-cFile"]:
    #         print(sys.argv[sys.argv.index(argumentOrValue)+1])


 
    #Initialize parser
    parser = argparse.ArgumentParser()
 
    # Adding optional argument
    parser.add_argument("-c", "--cFile", help = "C input file", required=TRUE)
    parser.add_argument("-d", "--dFile", help = "Directives input file",required=TRUE)
    parser.add_argument("-p", "--prjFile", help = "Prj. top file",required=TRUE)

 
    # Read arguments from command line
    args = parser.parse_args()
    
    filesDict = {}
    filesDict['cFile'] = args.cFile
    filesDict['dFile'] = args.dFile
    filesDict['prjFile'] = args.prjFile


    
    shaHill0 = HillClimbing(filesDict,'outShaHill.txt')
    shaHill0.writeSolutions()
