import copy
import json
import os
from pathlib import Path
from typing import List, Tuple, Union
from exceptions.timeExceededException import TimeExceededException
import xml.etree.ElementTree as ET

class Solution:
    
    def __init__(self,directives:dict = None):
        if directives:
            self.directives = copy.deepcopy(directives)
        else: 
            self.directives = {}
        self.period = None #in nano seconds
        results = {}
        results['FF'] = None
        results['DSP'] = None
        results['LUT'] = None
        results['BRAM'] = None
        results['resources'] = None
        results['latency'] = None
        self.results = results
        self.FF_VALUE = 1; self.LUT_VALUE = 2; self.DSP_VALUE = 345.68; self.BRAM_VALUE = 547.33

    def set_directives(self,directives:dict):
        """
        set directives used in this solution
        """
        self.directives = copy.deepcopy(directives)

    def set_one_result(self,key,value):
        self.results[key] = value

    def set_results(self,results:dict):
        self.results = results

    def set_results_with_results_list(self, results:list):
        for result in results:
            for index,key in enumerate(self.results):
                self.results[key] = result[index]
                   
    def build_solution_from_vitis_solution_path(self, vitis_solution_path:str, directives_file):
        self.solution_name = vitis_solution_path
        xml_path = os.path.join(vitis_solution_path, "reports", "csynth.xml")
        if os.path.exists(xml_path):  
            #read xml file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            x = root.find('AreaEstimates')
            x = x.find('Resources')
            self.results['FF'] =int(x.find('FF').text)
            self.results['DSP'] = int(x.find('DSP').text)
            self.results['LUT'] = int(x.find('LUT').text)
            self.results['BRAM'] = int(x.find('BRAM_18K').text)
            self.results['resources'] =  self.results['FF'] * self._FF_VALUE + self.results['LUT'] * self.LUT_VALUE + self.results['DSP'] * self.DSP_VALUE + self.results['BRAM'] * self.BRAM_VALUE    
            x = root.find('PerformanceEstimates')
            x = x.find('SummaryOfOverallLatency')
            try:
                self.results['latency'] = int(x.find('Average-caseLatency').text)
            except ValueError:
                raise ValueError("****UNDETERMINED LATENCY****")
        else:
            raise Exception("****Error in synthesis - NO Synthesis Results****")   
        solution_data_json = None
        for file in os.listdir(vitis_solution_path):
            if file.endswith("_data.json"):
                solution_data_json = os.path.join(vitis_solution_path, file)
                break
        if solution_data_json is None:
            raise FileNotFoundError("No solution_data.json file found in the specified path")
        solution_directives_tcl = self.extract_solution_directives(solution_data_json)
        with open(directives_file) as jsonFile:
            self.dse_config:dict =  json.load(jsonFile)
        directives = copy.deepcopy(self.dse_config['directives'])
        self.possible_directives = {}
        for key in directives:
            self.possible_directives[key] = directives[key]['possible_directives']
        self.directives = self.directives_tcl_to_solution(solution_directives_tcl,self.possible_directives)
        
    def directives_tcl_to_solution(self,directives_tcl, directives_groups):
        categorized = dict.fromkeys(directives_groups,'')
        for directive in directives_tcl:
            directive_keywords = set(directive.split())
            for key in directives_groups:
                #on directives file it has "" around the label of the directive but is not required to run
                for possible_directive in directives_groups[key]:
                    possible_directive_keywords = set(possible_directive.replace('"', '').split())
                    if directive_keywords == possible_directive_keywords:
                        categorized[key] = directive
                        break
        return categorized

    def extract_solution_directives(self,solution_data_json: Union[Path, str]) -> List[str]:
        with open(solution_data_json, "r") as f:
            data = json.load(f)
        directives = data["HlsSolution"]["DirectiveTcl"]
        return directives
