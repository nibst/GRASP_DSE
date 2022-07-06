import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd

class PlotMaker:
    _PLOT_PATH = './Plot/plot.jpg'
    def __init__(self,plotName,xAxis,yAxis,solutions):
        self.plotName = plotName
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.solutions = solutions
        self.plt = self.__createPlot()
    
    def __createPlot(self):
        listLUT = []
        listLat = []
        x_name = self.xAxis
        y_name = self.yAxis
        for element in self.solutions:
            resources = self.solutions[element].resultados[x_name]#self.solutions[element].resultados['resources']
            lat = self.solutions[element].resultados[y_name]
            listLUT.append(resources)
            listLat.append(lat)
        

        
        df = pd.DataFrame(list(zip(listLUT, listLat)),
                columns =[x_name, y_name])
        x = df[x_name]
        y = df[y_name]
        
        
        fig, ax = plt.subplots(1)
        plt.plot(listLUT,listLat,'s',)
        plt.title(self.plotName)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.xlim(left=0)
        plt.ylim(bottom=0)    
        return plt
        
    def savePlotAsJPG(self):
        self.plt.savefig(self._PLOT_PATH)
    def showPlot(self):
        self.plt.show()