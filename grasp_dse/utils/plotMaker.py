import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
class PlotMaker:
    _PLOT_PATH = './Plot/plot.jpg'
    def __init__(self,plotName,xAxis,yAxis):
        self.plotName = plotName
        SIZE = 16
        BIGGER_SIZE = 16
        plt.rc('font', size=SIZE)          # controls default text sizes
        plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=SIZE)    # legend fontsize
        plt.rc('figure', titlesize=SIZE)  # fontsize of the figure title
        self.xAxis = xAxis
        self.yAxis = yAxis
        #plt.rcParams["font.size"] =7
        self.fig, self.ax = plt.subplots()
        plt.title(self.plotName)
        plt.xlabel(self.xAxis)
        plt.ylabel(self.yAxis)
        plt.ylim(bottom=0)


        self.lns = []

    def plot(self,x,y,label=None,color=None,linewidth=None):
        ln = self.ax.plot(x,y,label=label,marker = 'o',color=color,linewidth=linewidth)
        self.lns.append(ln)
        plt.xlim(left=0)

    def twinx(self,label=None):
        self.ax=self.ax.twinx()
        self.ax.set_ylabel(label)
        
    def savePlotAsJPG(self,path):
        self.ax.savefig(self._PLOT_PATH)

    def showPlot(self):
        plt.show()

    def barPlot(self,x,y,label=None,color=None,width=None):
        ln = self.ax.bar(x,y,label=label,color=color,width=width)
        self.lns.append(ln)

    def ylim(self,bot,top):
        self.ax.set_ylim(bot,top)