from exhaustiveSearch import ExhaustiveSearch

h0 = ExhaustiveSearch('directivesFile.txt','output.txt')
permutation = h0.listOfDictsDirectives()
solutionsLst = h0.createSolutions(permutation)
#h0.writeSolutions(solutionsLst)
h0.writeSolutions(solutionsLst)
