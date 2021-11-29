from pathlib import Path
dierectiveMarker = '*'

def parseDirective(directivesLst):
    lst = []
    for element in directivesLst:
        directive =  element.split('\n')
        directive.remove('')
        lst.append(directive)
    return lst


def genDict(directivesLst):
    directivesDict = {}
    for directive in directivesLst:
        title = directive[0]
        specs = directive[1:]
        directivesDict[title] = specs
    return directivesDict

def fileParser(path):
    directivesTxt = Path(path).read_text()
    directivesLst = directivesTxt.split(dierectiveMarker)
    directivesLst = parseDirective(directivesLst)
    directiveDic = genDict(directivesLst)
    return directiveDic





