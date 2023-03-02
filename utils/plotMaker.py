import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
class PlotMaker:
    #TODO change to scatter plot
    _PLOT_PATH = './Plot/plot.jpg'
    def __init__(self,plotName,xAxis,yAxis):
        self.plotName = plotName
        self.xAxis = xAxis
        self.yAxis = yAxis
        plt.rcParams["font.size"] =7
        fig, ax = plt.subplots(1)
        plt.title(self.plotName)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        
    def createSolutionsPlot(self,solutions):
        listMetric1 = []
        listMetric2 = []
        x_name = self.xAxis
        y_name = self.yAxis
        for i in range(len(solutions)):
            try:
                metric1 = solutions[i].results[x_name]#self.solutions[element].results['resources']
                metric2 = solutions[i].results[y_name]
            except:
                metric1 = solutions[i].resultados[x_name]#self.solutions[element].results['resources']
                metric2 = solutions[i].resultados[y_name]
            listMetric1.append(metric1)
            listMetric2.append(metric2)
        
        plt.scatter(listMetric1,listMetric2)
        plt.xlim(left=0)
        plt.ylim(bottom=0) 

    def plot(self,x,y,label=None):
  
        plt.plot(x,y,label=label,marker = 'o')

        plt.legend()
        plt.xlim(left=0)
        plt.ylim(bottom=0) 

    def savePlotAsJPG(self,path):
        plt.savefig(self._PLOT_PATH)
    def showPlot(self):
        plt.show()