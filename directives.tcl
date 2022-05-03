set_directive_pipeline "main/main_label0"
set_directive_array_partition -type complete -dim 0 "main" indata
set_directive_pipeline "local_memcpy/local_memcpy_label3"
set_directive_loop_merge "sha_transform"
set_directive_pipeline "sha_update/sha_update_label4"
set_directive_unroll "sha_update/sha_update_label4"
