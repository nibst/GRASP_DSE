import copy
import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union
from domain.solution import Solution

class SolutionFactory:
    @staticmethod
    def create_solution_from_synthesis_xml(xml_path: str) -> Solution:
        """
        xml path is the synthesis report in xml
        """
        solution = Solution()
        solution.solution_name = "default_name"
        SolutionFactory._parse_xml_results(solution, xml_path)
        return solution

    @staticmethod
    def create_solution_from_vitis_path(vitis_solution_path: str, dse_config_file: str) -> Solution:
        """
        vitis_solution_path is our dataset solution path, that has a 'reports' dir inside it with the synthesis results
        dse_config_file is the benchmark specific set of all possible directives, its a json
        """
        solution = Solution()
        solution.solution_name = vitis_solution_path
        SolutionFactory._parse_xml_results(solution, os.path.join(vitis_solution_path, "reports", "csynth.xml"))
        solution_data_json = SolutionFactory._find_solution_data_json(vitis_solution_path)
        solution_directives_tcl = SolutionFactory._extract_solution_directives(solution_data_json)
        SolutionFactory._load_directives_config(solution, dse_config_file)
        solution.directives = SolutionFactory._directives_tcl_to_solution(solution_directives_tcl, solution.possible_directives)
        return solution

    @staticmethod
    def _parse_xml_results(solution: Solution, xml_path: str):
        if os.path.exists(xml_path):
            tree = ET.parse(xml_path)
            root = tree.getroot()
            x = root.find('AreaEstimates').find('Resources')
            solution.results['FF'] = int(x.find('FF').text)
            solution.results['DSP'] = int(x.find('DSP').text)
            solution.results['LUT'] = int(x.find('LUT').text)
            solution.results['BRAM'] = int(x.find('BRAM_18K').text)
            solution.results['resources'] = (solution.results['FF'] * solution.FF_VALUE +
                                             solution.results['LUT'] * solution.LUT_VALUE +
                                             solution.results['DSP'] * solution.DSP_VALUE +
                                             solution.results['BRAM'] * solution.BRAM_VALUE)
            x = root.find('PerformanceEstimates').find('SummaryOfOverallLatency')
            try:
                solution.results['latency'] = int(x.find('Average-caseLatency').text)
            except ValueError:
                raise ValueError("****UNDETERMINED LATENCY****")
        else:
            raise Exception(f"****Error in synthesis - NO Synthesis Results in {xml_path}****")
        

    @staticmethod
    def _find_solution_data_json(vitis_solution_path: str) -> str:
        for file in os.listdir(vitis_solution_path):
            if file.endswith("_data.json"):
                return os.path.join(vitis_solution_path, file)
        raise FileNotFoundError("No solution_data.json file found in the specified path")

    @staticmethod
    def _extract_solution_directives(solution_data_json: Union[Path, str]) -> list:
        with open(solution_data_json, "r") as f:
            data = json.load(f)
        return data["HlsSolution"]["DirectiveTcl"]

    @staticmethod
    def _load_directives_config(solution: Solution, dse_config_file: str):
        with open(dse_config_file) as json_file:
            solution.dse_config = json.load(json_file)
        directives = copy.deepcopy(solution.dse_config['directives'])
        solution.possible_directives = {key: directives[key]['possible_directives'] for key in directives}

    @staticmethod
    def _directives_tcl_to_solution(directives_tcl: list, directives_groups: dict) -> dict:
        categorized = dict.fromkeys(directives_groups, '')
        for directive in directives_tcl:
            directive_keywords = set(directive.split())
            for key in directives_groups:
                for possible_directive in directives_groups[key]:
                    possible_directive_keywords = set(possible_directive.replace('"', '').split())
                    if directive_keywords == possible_directive_keywords:
                        categorized[key] = directive
                        break
        return categorized