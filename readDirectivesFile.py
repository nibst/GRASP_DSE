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
        specs = ['']
        specs.extend(directive[1:])
        directivesDict[title] = specs
    return directivesDict

def fileParser(directivesTxt):
    directivesLst = directivesTxt.split(dierectiveMarker)
    directivesLst.remove('\n')
    directivesLst.remove('')
    directivesLst = parseDirective(directivesLst)
    directiveDic = genDict(directivesLst)
    return directiveDic






