set_directive_unroll -factor 256 "computeGradient/GRAD"
set_directive_unroll -factor 256 "updateParameter/UPDATE"
set_directive_pipeline "SgdLR_sw/TRAINING_INST"
set_directive_unroll -factor 512 "SgdLR_sw/TRAINING_INST"
set_directive_array_partition -type block -factor 512 -dim 1 "SgdLR_sw" gradient
