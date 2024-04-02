
############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project Raise_dse
set_top example
add_files {./benchmark_testing/synthesizable_input.cpp }
open_solution "solution1"
set_part {xcvu35p-fsvh2104-1-e}
create_clock -period 8 -name default
source "./domain/directives.tcl"
set ::LLVM_CUSTOM_OPT /home/nikolas/Documents/IC_Things/hls-llvm-project/hls-build/bin/opt
set ::LLVM_CUSTOM_INPUT approx_results/exact_design/synthesizable_input.MDUpdated.IOFCallRemoved.bc
set ::LLVM_CUSTOM_CMD {$LLVM_CUSTOM_OPT  $LLVM_CUSTOM_INPUT -o $LLVM_CUSTOM_OUTPUT}
csynth_design
exit
