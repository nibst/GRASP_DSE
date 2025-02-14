

from grasp_dse.domain.solution import Solution
from grasp_dse.predictor.estimators.estimator import Estimator
import os
import pickle

from grasp_dse.predictor.estimators.randomforest.randomForest import RandomForestEstimator


def gather_dataset(path):
    solutions = []
    for solution_dir in os.listdir(path):
        solution_path = os.path.join(path, solution_dir)
        if os.path.isdir(solution_path):
            if os.path.exists(solution_path):
                solution = Solution()
                solution.build_solution_from_vitis_solution_path(solution_path)
                solutions.append(solution)
    return solutions
    
def train(path,estimator:Estimator):
    x = gather_dataset(path)
    # estimator.trainModel(gather_dataset(path))
    # with open('./models/new/', 'wb') as modelFile:
    #     pickle.dump(estimator,modelFile)

if __name__ == "__main__": 
    path = "./dataset/AES/"
    estimator = RandomForestEstimator("./directives_files/aes.json")
    train(path)