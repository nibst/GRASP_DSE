from typing import List

from domain.solution import Solution


class HeuristicSolutions:
    def __init__(self, heuristic_name: str, solutions_timestamps_per_benchmark: dict[list[List[Solution]]]):
        self.heuristic_name = heuristic_name
        self.solutions_timestamps_per_benchmark = solutions_timestamps_per_benchmark

    def get_timestamps(self, benchmark: str) -> List[List[Solution]]:
        """
        Get the solutions for a specific benchmark.
        
        :param benchmark: The name of the benchmark.
        :return: A list of timestamps for the specified benchmark.
        """
        return self.solutions_timestamps_per_benchmark.get(benchmark, [])
    def get_name(self) -> str:
        """
        Get the name of the heuristic.
        
        :return: The name of the heuristic.
        """
        return self.heuristic_name