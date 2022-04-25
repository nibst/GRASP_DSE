from ast import arguments
from pickle import TRUE
<<<<<<< Updated upstream

from setuptools import Require
from greedy import Greedy
from hillClimbing0 import HillClimbing
import argparse



=======
from hillClimbing0 import HillClimbing
import argparse 
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd


import random
>>>>>>> Stashed changes
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
    

    
<<<<<<< Updated upstream
    shaHill0 = HillClimbing(filesDict,'directives.tcl')
    shaHill0.writeSolutionsDict()
=======
    heuristic = HillClimbing(filesDict,'directives.tcl')
    #shaHill0.writeSolutionsDict() 
    numberOfSol = len(heuristic.solutions.keys()) 
    
    listLUT = []
    listLat = []

    for element in heuristic.solutions:
        lut = heuristic.solutions[element].resultados['LUT']
        lat = heuristic.solutions[element].resultados['latency']
        listLUT.append(lut)
        listLat.append(lat)
    

    x_name = 'LUT'
    y_name = 'Latency'
    df = pd.DataFrame(list(zip(listLUT, listLat)),
               columns =[x_name, y_name])
    x = df[x_name]
    y = df[y_name]
    
    
    fig, ax = plt.subplots(1)
    plt.plot(listLUT,listLat,'--r',)
    plt.plot(listLUT,listLat,'s',)
    plt.title('SHA')
    plt.xlabel(x_name)
    plt.ylabel(y_name)

    hText = 0.8
    for solution in heuristic.solutions:
        plt.figtext(0.05, hText,solution, fontsize=9)
        plt.figtext(0.05 , hText-0.05, 'Latency:', fontsize=8)
        plt.figtext(0.15 , hText-0.05, listLat[solution-1], fontsize=8)
        plt.figtext(0.05 , hText-0.1, '#LUT:', fontsize=8)
        plt.figtext(0.15 , hText-0.1, listLUT[solution-1], fontsize=8)
        hText -= 0.15  


    plt.subplots_adjust(left=0.35)
    plt.show()
    
    
    #shaHill0.teste()
>>>>>>> Stashed changes
   
