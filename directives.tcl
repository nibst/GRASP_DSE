set_directive_unroll "local_memcpy/local_memcpy_label3"
set_directive_pipeline "sha_update/sha_update_label4"
set_directive_unroll -factor 32 "sha_update/sha_update_label4"
set_directive_pipeline "sha_transform/sha_transform_label1"
set_directive_unroll -factor 8 "sha_transform/sha_transform_label1"
set_directive_pipeline "sha_transform/sha_transform_label3"
set_directive_pipeline "sha_transform/sha_transform_label4"
set_directive_unroll -factor 16 "sha_transform/sha_transform_label4"
set_directive_unroll -factor 16 "sha_transform/sha_transform_label5"
set_directive_pipeline "sha_transform/sha_transform_label6"
set_directive_unroll -factor 4 "sha_transform/sha_transform_label6"
set_directive_array_partition -type complete -dim 1 "sha_transform" W
set_directive_inline "local_memset"
set_directive_array_partition -type complete -dim 1 "sha_transform" sha_info_digest
