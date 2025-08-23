@echo off
set PATH=%PATH%;C:\Xilinx\Vitis_HLS\2023.1\bin
call C:\Xilinx\Vitis_HLS\2023.1\settings64.bat
vitis_hls -f .\domain\script.tcl