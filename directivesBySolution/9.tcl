########## 
#Solucao de indice 9
##########
pipeline main_label0:set_directive_pipeline "main/main_label0"
array_partition main:set_directive_array_partition -type block -factor 100 -dim 0 "main" indata
pipeline local_memcpy_label3:set_directive_pipeline "local_memcpy/local_memcpy_label3"
loop_merge sha_transform:set_directive_loop_merge "sha_transform"
pipeline sha_update_label4:set_directive_pipeline "sha_update/sha_update_label4"
unroll sha_update_label4:
