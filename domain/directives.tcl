set_directive_inline "local_memset"
set_directive_unroll  "local_memset/local_memset_label0"
set_directive_array_partition -type cyclic -factor 2 -dim 1 "sha_transform" sha_info_digest
