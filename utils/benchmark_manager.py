import os
import pickle
from typing import List

from domain.solution import Solution


class BenchmarkManager:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def __get_ordered_saves_paths(self, path):
        dir_list: list = os.listdir(path)
        dir_list.sort(key=lambda x: int(x[len(x) - 1]))
        relative_paths = list(map(lambda x: path + x, dir_list))
        return relative_paths

    def __save_files_to_timestamps_list(self, paths: list):
        list_of_solutions_list: List[List[Solution]] = []
        for path in paths:
            with open(path, 'rb') as file:
                solutions = pickle.load(file)
            list_of_solutions_list.append(solutions)
        return list_of_solutions_list

    def path_to_lists_of_solutions_timestamps(self, path):
        ordered_paths = self.__get_ordered_saves_paths(path)
        return self.__save_files_to_timestamps_list(ordered_paths)
    
    def load_solutions_timestamps(self, heuristic_name: str, benchmark: str, file_path = None, timestamp_limit: int = 10) -> List[Solution]:
        if file_path:
            path = file_path
        else:
            path = os.path.join(self.base_path, f"saves/{heuristic_name}_{benchmark}_4h/")
            if not os.path.exists(path):
                # if 4h path does not exist, try 8h path
                path = os.path.join(self.base_path, f"saves/{heuristic_name}_{benchmark}_8h/")
        timestamps = self.path_to_lists_of_solutions_timestamps(path)
        # the number of timestamps often is one less than the number desired for some reason, 
        # than we just assume the last timestamp as the solutions from the completed heuristic which is saved in dse/
        if len(timestamps) < timestamp_limit:
            last_timestamp = self.complete_time_stamps(heuristic_name, benchmark)
            if last_timestamp:
                timestamps.append(last_timestamp)
            else:
                timestamps.append(timestamps[-1]) # just copy the last time stamp as its final timestamp
        return timestamps

    def complete_time_stamps(self, heuristic_name: str, benchmark: str) -> List[Solution]:
        try:
            with open(f"{self.base_path}/dse/{heuristic_name}_{benchmark}4h_preTrained", "rb") as f:
                heuristic = pickle.load(f)
        except FileNotFoundError:
            with open(f"{self.base_path}/dse/{heuristic_name}_{benchmark}8h_preTrained", "rb") as f:
                heuristic = pickle.load(f)
        return heuristic.solutions

