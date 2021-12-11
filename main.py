from bestOfEach import BestOfEach
from exhaustiveSearch import ExhaustiveSearch

h0 = ExhaustiveSearch('directivesFile.txt','output.txt')
h0.writeSolutions()
h1 = BestOfEach('directivesFile.txt','outBestofEach.txt')
