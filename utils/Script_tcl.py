from string import Template

def generateScript(cFile, prjFile):
     filesSeparatedBySpace = ""
     for file in cFile:
          filesSeparatedBySpace = (filesSeparatedBySpace+ file + " ")
     subtituicoes = {
     'fun_top': prjFile,
     'arq_cpp': filesSeparatedBySpace, 
     }


     with open('./domain/script.tcl.txt', 'r') as f:
          src = Template(f.read())
     result = src.substitute(subtituicoes)

     # open text file
     text_file = open('./domain/script.tcl' , 'w')
 
     # write string to file
     text_file.write(result)

     # close file
     text_file.close()
     