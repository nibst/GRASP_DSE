set_directive_unroll -factor 2 "fft1D_512/loop1"
set_directive_unroll -factor 16 "fft1D_512/loop3"
set_directive_unroll "fft1D_512/loop4"
set_directive_unroll -factor 2 "fft1D_512/loop5"
set_directive_unroll -factor 2 "fft1D_512/loop6"
set_directive_unroll -factor 2 "fft1D_512/loop7"
set_directive_unroll "fft1D_512/loop8"
set_directive_unroll -factor 32 "fft1D_512/loop9"
set_directive_unroll -factor 32 "fft1D_512/loop10"
set_directive_unroll -factor 2 "fft1D_512/loop11"
set_directive_pipeline "fft1D_512/loop2"
set_directive_pipeline "fft1D_512/loop7"
set_directive_pipeline "fft1D_512/loop9"
set_directive_pipeline "fft1D_512/loop10"
set_directive_pipeline "fft1D_512/loop11"
set_directive_array_partition -type cyclic -factor 2 -dim 0 "fft1D_512" reversed
set_directive_array_partition -type block -factor 64 -dim 0 "fft1D_512" DATA_y
set_directive_array_partition -type block -factor 4 -dim 0 "fft1D_512" smem
set_directive_array_partition -type block -factor 4 -dim 0 "fft1D_512" data_x
set_directive_array_partition -type complete -dim 0 "fft1D_512" data_y
10
