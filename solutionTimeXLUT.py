from solution import Solution
import time
from datetime import timedelta
class SolutionTimeXLUT:

    def __init__(self,solution):
        self.solution=solution
        self.time = self.runSynthesisTXL()
        

    def runSynthesisTXL(self):

        start_time = time.monotonic()
        self.solution.runSynthesis()
        end_time = time.monotonic()
        timeElapsed = timedelta(seconds=end_time - start_time)
        lut = self.solution.resultados['LUT']

        pair = (timeElapsed,lut)


        return pair

