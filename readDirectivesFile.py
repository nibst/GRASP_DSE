from pathlib import Path

directiveMarker = '*'


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
    
    directivesLst = directivesTxt.split(directiveMarker) 
    directivesLst = list(filter(lambda x: x!= '', directivesLst))
    directivesLst = parseDirective(directivesLst)
    directivesLst = [e for e in directivesLst if e]
    directiveDic = genDict(directivesLst)
    
    return directiveDic



