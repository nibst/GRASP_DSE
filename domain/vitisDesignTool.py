from random import randrange
from domain.desingTool import DesignTool
from domain.solution import Solution
import xml.etree.ElementTree as ET
import os.path
import shutil
import time
import subprocess
import psutil
import sys
from domain.solution_factory import SolutionFactory
from exceptions.timeExceededException import TimeExceededException
from utils.Script_tcl import generate_script_for_implementation, generateScript

class Vitis(DesignTool):
    
    def __init__(self, maxRAMUsage = 50, directivesFilename = './domain/directives.tcl'):
        self._MAX_RAM_USAGE = maxRAMUsage #in percentage
        self._DIRECTIVES_FILENAME = directivesFilename
        self._PROCESSNAME = 'vitis_hls'
        self._SCRIPT_PATH = './domain/callVitis.sh'
        if sys.platform == 'win32':
            self._PROCESSNAME = 'vitis_hls.exe'
            self._SCRIPT_PATH = './domain/callVitis.bat'
        
    def runSynthesis(self, solution: Solution, c_files, top_func, timeLimit = None, solutionSaver= None, run_implementation=False):
        self.__killOnGoingVitisProcessIfAny()    
        #if not especified, there is infinite time to run synthesis
        if timeLimit is None:
            timeLimit = float('inf')
        if timeLimit<=0:
            raise Exception(f"****{self._PROCESSNAME} has exceed max time usage****")
        self.__writeDirectivesIntoFile(solution.directives)
        if run_implementation:
            generate_script_for_implementation(c_files,top_func,solution.period)
        else:
            generateScript(c_files,top_func,solution.period)
        print('Running Synthesis...')
        #vitis call using subprocess
        subprocess.Popen([self._SCRIPT_PATH])
        self.__monitorVitisProcess(timeLimit, solutionSaver)

        synthesis_xml='./Raise_dse/solution1/syn/report/csynth.xml'
        if run_implementation:
            impl_xml='./Raise_dse/solution1/impl/report/verilog/export_syn.xml'
            results = self.get_results_from_implementation(solution,impl_xml)
            results['latency'] = self.get_latency_from_synthesis(synthesis_xml)
            results['resources'] = self.compute_resources(results,synthesis_xml)
        else:
            results = self.getResultsFromSynthesis(solution,synthesis_xml)
            results['resources'] = self.compute_resources(results,synthesis_xml)
        for key in results:
            solution.set_one_result(key, results[key])
        print (results)
        return solution

    def __writeDirectivesIntoFile(self,directives):
        directivesFile = open(self._DIRECTIVES_FILENAME, "w")
        for value in directives.values():
            if value != '' and value is not None:
                directivesFile.write(value + '\n')
            print(value)
        directivesFile.close()  

    def __killOnGoingVitisProcessIfAny(self):
        mydir='./Raise_dse'
        while os.path.exists(mydir):
            time.sleep(3)
            try:
                shutil.rmtree(mydir)
            except Exception as error:
                print(error)
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._PROCESSNAME:
                    proc.kill()
                    break        

    def __monitorVitisProcess(self, timeLimit, solutionSaver):
        #testing if the synthesis ended
        vitisIsRunning = True   
        start = time.time()
        while vitisIsRunning:
            #time between checking if the process is still running
            time.sleep(3)
            vitisIsRunning = False
            for proc in psutil.process_iter(['name']):
                if proc.name() == self._PROCESSNAME:
                    vitisIsRunning = True
                    #check memory usage
                    try:
                        memoryUse = proc.memory_percent()
                    except Exception as e:
                        print(e)
                        break
                    if memoryUse > self._MAX_RAM_USAGE:
                        proc.kill()   
                        raise Exception(f"****{self._PROCESSNAME} has exceed max RAM usage****")
                    #check time usage 
                    if time.time()-start >= timeLimit:
                        proc.kill()   
                        raise TimeExceededException(f"****{self._PROCESSNAME} has exceed max time usage****")
                    if solutionSaver:
                        solutionSaver.save(None,'./time_stamps/timeStampFiller')
                    break
    def get_latency_from_synthesis(self, synthesis_report_xml_path:str):
        latency = None
        if os.path.exists(synthesis_report_xml_path):
            print("Synthesis ended")
            #read xml file
            tree = ET.parse(synthesis_report_xml_path)
            root = tree.getroot()
            x = root.find('PerformanceEstimates')
            x = x.find('SummaryOfOverallLatency')
            try:
                latency = int(x.find('Average-caseLatency').text)
            except ValueError:
                raise ValueError("****UNDETERMINED LATENCY****")
        else:
            raise Exception("****Error in synthesis - NO Synthesis Results****")   
        return latency
    def get_results_from_implementation(self, solution:Solution, impl_report_xml_path:str):
        results = {}
        if os.path.exists(impl_report_xml_path):
            print("Implementation ended")
            #read xml file
            tree = ET.parse(impl_report_xml_path)
            root = tree.getroot()
            x = root.find('AreaReport')
            x = x.find('Resources')
            results['FF'] =int(x.find('FF').text)
            results['DSP'] = int(x.find('DSP').text)
            results['LUT'] = int(x.find('LUT').text)
            results['BRAM'] = int(x.find('BRAM').text)
        else:
            raise Exception("****Error in implementation - NO Implementation Results****")   
        return results
    def getResultsFromSynthesis(self, solution:Solution, xmlPath:str):   
        results = {}
        # SolutionFactory.create_solution_from_vitis_path(vitis_solution_path, directives_file)
        if os.path.exists(xmlPath):  
            print("Synthesis ended")
            #read xml file
            tree = ET.parse(xmlPath)
            root = tree.getroot()

            x = root.find('AreaEstimates')
            x = x.find('Resources')
            results['FF'] =int(x.find('FF').text)
            results['DSP'] = int(x.find('DSP').text)
            results['LUT'] = int(x.find('LUT').text)
            results['BRAM'] = int(x.find('BRAM_18K').text)
            results['latency'] = self.get_latency_from_synthesis(xmlPath)
        else:
            raise Exception("****Error in synthesis - NO Synthesis Results****")   
        return results    

    def compute_resources(self,results,synthesis_xml_path):
        """
        returns the resources of a solution, based on the results and the values of resources
        """
        available_resources= self.get_available_resources(synthesis_xml_path)
        resources_values = self.get_resources_values(available_resources)
        resources = 0
        for resource in resources_values:
            resources += results[resource] * resources_values[resource]
        return resources
    def get_available_resources(self,xml_path):
        available_resources = {}
        tree = ET.parse(xml_path)
        root = tree.getroot()

        x = root.find('AreaEstimates')
        x = x.find('AvailableResources')
        available_resources['FF'] =int(x.find('FF').text)
        available_resources['DSP'] = int(x.find('DSP').text)
        available_resources['LUT'] = int(x.find('LUT').text)
        available_resources['BRAM'] = int(x.find('BRAM_18K').text)
        return available_resources
   
    def get_resources_values(self,available_resources):
        """
        returns the values of resources, based on the available resources.
        This is computed by dividing the most abundant resource by each other resources
        So e.g if it has 10 FF (its the most abundant resource) and 5 LUT, the value of FF is 1 and the value of LUT is 2
        """
        resources_values = {}
        most_abundant_resource = max(available_resources, key=available_resources.get)
        for resource in available_resources:
            resources_values[resource] = available_resources[most_abundant_resource] / available_resources[resource]
        return resources_values
