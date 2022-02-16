########## 
#Solucao de indice 3
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:
