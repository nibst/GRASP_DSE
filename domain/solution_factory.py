import copy
import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union
from domain.solution import Solution
from utils import parser

class SolutionFactory:
    @staticmethod
    def create_solution_from_synthesis_xml(xml_path: str) -> Solution:
        """
        xml path is the synthesis report in xml
        """
        solution = Solution()
        solution.solution_name = "default_name"
        SolutionFactory._parse_hls_synthesis_results(solution, xml_path)
        return solution

    @staticmethod
    def create_solution_from_vitis_path(vitis_solution_path: str, dse_config_file: str, filtered:bool = False, is_implementation: bool = True) -> Solution:
        """
        vitis_solution_path is solution path
        dse_config_file is the benchmark specific set of all possible directives, its a json
        if filtered than the solution path will have a 'reports' directory with all impl and hls reports
        if not filtered thatn it has the default vitis structure
        if is_implementation is True, then the implementation report will be used, else the synthesis report will be used
        """
        solution = Solution()
        solution.solution_name = vitis_solution_path
        if is_implementation:
            resources_utilization = parser.extract_impl_utilization(vitis_solution_path, filtered) 
        else:
            resources_utilization = parser.extract_hls_utilization(vitis_solution_path,filtered)
        latency = parser.extract_hls_cc_report(vitis_solution_path, filtered)
        results = resources_utilization | {"latency" : latency}
        results["resources"] = parser.compute_snru(results, vitis_solution_path, filtered)
        solution.set_results(results)

        are_valid_results , error = solution.has_valid_results()
        if not are_valid_results:
            raise error
        
        solution_data_json = SolutionFactory._find_solution_data_json(vitis_solution_path)
        solution_directives_tcl = SolutionFactory._extract_solution_directives(solution_data_json)
        SolutionFactory._load_directives_config(solution, dse_config_file)
        solution.directives = SolutionFactory._directives_tcl_to_solution(solution_directives_tcl, solution.possible_directives)
        return solution

    #TODO pass some of these static methods to the parser file
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