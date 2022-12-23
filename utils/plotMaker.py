import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd

class PlotMaker:
    #TODO change to scatter plot
    _PLOT_PATH = './Plot/plot.jpg'
    def __init__(self,plotName,xAxis,yAxis):
        self.plotName = plotName
        self.xAxis = xAxis
        self.yAxis = yAxis
        
        self.plt = plt
        fig, ax = self.plt.subplots(1)
        
    def createPlot(self,solutions):
        listLUT = []
        listLat = []
        x_name = self.xAxis
        y_name = self.yAxis
        for i in range(len(solutions)):
            try:
                resources = solutions[i].results[x_name]#self.solutions[element].results['resources']
                lat = solutions[i].results[y_name]
            except:
                resources = solutions[i].resultados[x_name]#self.solutions[element].results['resources']
                lat = solutions[i].resultados[y_name]
            listLUT.append(resources)
            listLat.append(lat)
        

        
        df = pd.DataFrame(list(zip(listLUT, listLat)),
                columns =[x_name, y_name])
        x = df[x_name]
        y = df[y_name]
        
        
        
        self.plt.plot(listLUT,listLat,'s',)
        self.plt.title(self.plotName)
        self.plt.xlabel(x_name)
        self.plt.ylabel(y_name)
        self.plt.xlim(left=0)
        self.plt.ylim(bottom=0)    
        return self.plt
        
    def savePlotAsJPG(self):
        self.plt.savefig(self._PLOT_PATH)
    def showPlot(self):
        self.plt.show()