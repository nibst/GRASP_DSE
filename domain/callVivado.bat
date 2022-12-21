@echo off
set PATH=%PATH%;C:\Xilinx\Vivado\2020.1\bin
call C:\Xilinx\Vivado\2020.1\settings64.bat
vivado_hls -f .\domain\script.tcl
