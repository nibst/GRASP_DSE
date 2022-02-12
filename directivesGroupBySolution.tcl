########## 
#Solucao de indice 0
##########
pipeline main_label0:
########## 
#Solucao de indice 1
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
########## 
#Solucao de indice 2
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:
########## 
#Solucao de indice 3
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:
########## 
#Solucao de indice 4
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
########## 
#Solucao de indice 5
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
loop_merge sha_transform:
########## 
#Solucao de indice 6
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
loop_merge sha_transform:set_directive_loop_merge "sha_transform"
########## 
#Solucao de indice 7
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
loop_merge sha_transform:set_directive_loop_merge "sha_transform"
pipeline sha_update_label4:
########## 
#Solucao de indice 8
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
loop_merge sha_transform:set_directive_loop_merge "sha_transform"
pipeline sha_update_label4:set_directive_pipeline "sha_update/sha_update_label4"
########## 
#Solucao de indice 9
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 10 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
loop_merge sha_transform:set_directive_loop_merge "sha_transform"
pipeline sha_update_label4:set_directive_pipeline "sha_update/sha_update_label4"
unroll sha_update_label4:
