
############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project Raise_dse
set_top sha_stream
add_files {./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c }
open_solution "solution1"
set_part {xcvu9p-flgb2104-1-e}
create_clock -period 8 -name default
source "directives.tcl"
csynth_design
exit
