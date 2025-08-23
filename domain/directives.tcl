set_directive_unroll md_kernel/loop_i -factor 8
set_directive_unroll md_kernel/loop_j -factor 8
set_directive_pipeline md_kernel/loop_j
set_directive_array_partition md_kernel -type cyclic -dim 0 -factor 4 force_x
set_directive_array_partition md_kernel -type block -dim 0 -factor 16 force_y
set_directive_array_partition md_kernel -type cyclic -dim 0 -factor 2 position_x
set_directive_array_partition md_kernel -type block -dim 0 -factor 8 position_y
set_directive_array_partition md_kernel -type cyclic -dim 0 -factor 16 position_z
set_directive_array_partition md_kernel -type cyclic -dim 0 -factor 2 NL
set_directive_loop_merge md_kernel/loop_i
