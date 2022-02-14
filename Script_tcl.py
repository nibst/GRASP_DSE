from string import Template

print("entre o nome do projeto:")
nome_projeto=input()
print("entre qual a função topo:")
fun_top=input()
print("Entre o nome do arquivo.cpp:")
arq_cpp=input()
print("entre o nome da solução:")
solution_name=input()
print("entre com o caminho das diretivas:")
fonte_diretivas=input()

subtituicoes = {
     'nome_projeto': nome_projeto,
     'fun_top': fun_top,
     'arq_cpp': arq_cpp,
     'solution_name':solution_name,
     'fonte_diretivas': fonte_diretivas

 }


with open('script.tcl.txt', 'r') as f:
     src = Template(f.read())
     result = src.substitute(subtituicoes)

# open text file
text_file = open(r'C:\Users\Nathan\Desktop\teste.tcl' , 'w')

# write string to file
text_file.write(result)

# close file
text_file.close()