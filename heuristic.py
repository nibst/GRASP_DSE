import readDirectivesFile

dict = readDirectivesFile.fileParser('directivesFile.txt')
for element in dict:
    print(element)
    print(dict[element])
