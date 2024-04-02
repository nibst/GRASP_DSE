
from domain.vitisDesignTool import Vitis
from domain.vivadoDesignTool import Vivado
from domain.mockDesignTool import MockDesignTool
class DesignToolFactory():
    @staticmethod
    def getDesignTool(designTool:str):
        if designTool == "vitis":
            return Vitis()
        elif designTool == "vivado":
            return Vivado()
        elif designTool == "mock":
            return MockDesignTool()
        #default design tool
        else: return Vivado()
