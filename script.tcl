############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
############################################################
open_project $nome_projeto
set_top $fun_top
add_files $arq_cpp
open_solution "$solution_name"
set_part {xcvu9p-flgb2104-1-e}
create_clock -period 8 -name default
source "$fonte_diretivas"
csim_design
csynth_design
cosim_design
export_design -format ip_catalog
