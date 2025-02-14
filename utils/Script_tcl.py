from string import Template

def generateScript(cFile, prjFile):
     filesSeparatedBySpace = ""
     for file in cFile:
          filesSeparatedBySpace = (filesSeparatedBySpace+ file + " ")
     substitutions = {
     'fun_top': prjFile,
     'arq_cpp': filesSeparatedBySpace, 
     }


     with open('./domain/script.tcl.txt', 'r') as f:
          src = Template(f.read())
     result = src.substitute(substitutions)

     # open text file
     text_file = open('./domain/script.tcl' , 'w')
 
     # write string to file
     text_file.write(result)

     # close file
     text_file.close()
def generateScriptWithInputIR(cFile, prjFile, inputIR, llvmOpt):
     filesSeparatedBySpace = ""
     for file in cFile:
          filesSeparatedBySpace = (filesSeparatedBySpace+ file + " ")
     substitutions = {
     'fun_top': prjFile,
     'arq_cpp': filesSeparatedBySpace, 
     'input'  : inputIR,
     'opt_path'   : llvmOpt,
     'LLVM_CUSTOM_OPT' : '$LLVM_CUSTOM_OPT',
     'LLVM_CUSTOM_INPUT' : '$LLVM_CUSTOM_INPUT',
     'LLVM_CUSTOM_OUTPUT' : '$LLVM_CUSTOM_OUTPUT'
     }

     with open('./domain/scriptWithInputIR.tcl.txt', 'r') as f:
          src = Template(f.read())
     result = src.substitute(substitutions)

     # open text file
     text_file = open('./domain/script.tcl' , 'w')
     
     # write string to file
     text_file.write(result)

     # close file
     text_file.close()