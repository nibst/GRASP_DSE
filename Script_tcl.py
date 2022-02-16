from string import Template



def generateScript(self,diretivas, cFile, prjFile):

     subtituicoes = {
     'fun_top': prjFile,
     'arq_cpp': cFile,
     }


     with open('script.tcl.txt', 'r') as f:
          src = Template(f.read())
     result = src.substitute(subtituicoes)

     # open text file
     text_file = open('script.tcl' , 'w')
 
     # write string to file
     text_file.write(result)

     # close file
     text_file.close()