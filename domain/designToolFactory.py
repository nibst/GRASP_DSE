
from domain.vitisDesignTool import Vitis
from domain.vivadoDesignTool import Vivado

class DesignToolFactory():
    @staticmethod
    def getDesignTool(designTool:str):
        if designTool == "vitis":
            return Vitis()
        elif designTool == "vivado":
            return Vivado()
        #default design tool
        else: return Vivado()
