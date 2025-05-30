from typing import List

from domain.solution import Solution


class HeuristicSolutions:
    def __init__(self, heuristic_name: str, solutions_timestamps_per_benchmark: dict[list[List[Solution]]]):
        self.heuristic_name = heuristic_name
        self.solutions_timestamps_per_benchmark = solutions_timestamps_per_benchmark