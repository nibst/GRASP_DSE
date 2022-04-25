############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project Raise_dse
<<<<<<< Updated upstream
<<<<<<< Updated upstream
set_top test.prj
add_files ['hid.c', 'example.c']
=======
set_top sha_stream
add_files {benchmarks/sha/sha.c }
>>>>>>> Stashed changes
=======
set_top sha_stream
add_files {benchmarks/sha/sha.c }
>>>>>>> Stashed changes
open_solution "solution1"
set_part {xcvu9p-flgb2104-1-e}
create_clock -period 8 -name default
source "..\directives.tcl"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
