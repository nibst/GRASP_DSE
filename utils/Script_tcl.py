from string import Template

def generateScript(cFile, topFunc, period = 8):
     filesSeparatedBySpace = ""
     for file in cFile:
          filesSeparatedBySpace = (filesSeparatedBySpace+ file + " ")
     substitutions = {
     'fun_top': topFunc,
     'arq_cpp': filesSeparatedBySpace,
     'period' :  period
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
def generateScriptWithInputIR(cFile, topFunc, inputIR, llvmOpt):
     filesSeparatedBySpace = ""
     for file in cFile:
          filesSeparatedBySpace = (filesSeparatedBySpace+ file + " ")
     substitutions = {
     'fun_top': topFunc,
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

def generate_script_for_implementation(c_files, top_function, period = 8):
     files_separated_by_space = ""
     for file in c_files:
          files_separated_by_space = (files_separated_by_space+ file + " ")
     substitutions = {
     'fun_top': top_function,
     'arq_cpp': files_separated_by_space,
     'period' :  period
     }


     with open('./domain/script_template_implementation.txt', 'r') as f:
          src = Template(f.read())
     result = src.substitute(substitutions)

     # open text file
     text_file = open('./domain/script.tcl' , 'w')
 
     # write string to file
     text_file.write(result)

     # close file
     text_file.close()