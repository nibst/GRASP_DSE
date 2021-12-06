from pathlib import Path
dierectiveMarker = '*'

def parseDirective(directivesLst):
    lst = []
    for element in directivesLst:
        directive =  element.split('\n')
        directive = list(filter(lambda x: x!= '', directive))
        lst.append(directive)
    return lst

def genDict(directivesLst):
    directivesDict = {}
    for directive in directivesLst:
        title = directive[0]
        specs = ['']                            #inicializa lista com valor '', especificando diretiva nao utilizada              
        specs.extend(directive[1:])             #
        directivesDict[title] = specs           #e.g. dicionario[pipeline] = ['',pipe 1, pipe2]
    return directivesDict

def fileParser(directivesTxt):
    directivesLst = directivesTxt.split(dierectiveMarker)       #Gera uma lista de separada pelo marcador '*'
    directivesLst.remove('\n')                                  # e remove dela item inúteis advindos do parsing
    directivesLst.remove('')                                                 
    directivesLst = parseDirective(directivesLst)               #e gera uma lista de listas de diretivas
                                                                #e.g. [['pipeline', 'pipe 1', 'pipe 2'], [...],...]
    directiveDic = genDict(directivesLst)
    
        #metodo retorna um dicionario com o nome da diretiva como
        #key e lista de especificações como valores
    return directiveDic






