from ast import arguments
from greedy import Greedy
from hillClimbing0 import HillClimbing
import sys, os, subprocess, argparse

# h0 = HillClimbing('test.txt','outTest.txt')
# h0.writeSolutions()

# h1 = HillClimbing('arq_input_aes.txt','outAesHill.txt')
# h1.writeSolutions()

# h2 = HillClimbing('arq_input_gsm.txt','outGsmHill.txt')
# h2.writeSolutions()

# h3 = HillClimbing('arq_input_sha.txt','outShaHill.txt')
# h3.writeSolutions()

# h4 = Greedy('arq_input_sha.txt','outShaGreedy.txt')
# h4.writeSolutions()
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
    parser.add_argument("-c", "--cFile", help = "C input file")
    parser.add_argument("-d", "--dFile", help = "Directives input file")
    parser.add_argument("-p", "--prjFile", help = "Prj. top file")

 
    # Read arguments from command line
    args = parser.parse_args()
 
    if args.cFile:
        print("Using: % s" % args.cFile)
    if args.dFile:
        print("Directives are in: % s" % args.dFile)
    if args.prjFile:
        print("Using: % s" % args.prjFile)