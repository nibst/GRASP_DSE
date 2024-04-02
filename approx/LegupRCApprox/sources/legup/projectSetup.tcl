# to run:
# quartus_sh -t setup_proj.tcl <family> <board> <verilog_name> <top_level_module> [<dbg_dir>]

project_new top -overwrite

set family [lindex $quartus(args) 0]
set board  [lindex $quartus(args) 1]
set where  [file normalize [file dirname [info script]]/../boards]
set search_path [file normalize [file dirname [info script]]/../tiger/processor/altera_libs]

set board_qsf  $where/$family/$board/$board.qsf
set family_qsf $where/$family/$family.qsf
set common_qsf $where/common.qsf

# Debugger files
if {[llength $quartus(args)] > 4} {
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/hlsd.v
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/trigger.v
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/trace.v
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/comm.v
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/uart_control.v
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/uart_altera.v
	set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/rams_altera.v

	if {$board eq "DE4"} {
		set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/clockbuf_stratixiv.v
	} elseif {$board eq "DE2"} {
		set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/clockbuf_cycloneii.v
    } elseif {$board eq "CycloneIIAuto"} {
		set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 4]/rtl/clockbuf_cycloneii.v
	} else {
		puts "Board not supported for debugging"
		exit -1
	}
}

set_global_assignment -name SOURCE_FILE [lindex $quartus(args) 2].v
set_global_assignment -name SDC_FILE [lindex $quartus(args) 2].sdc
set_global_assignment -name TOP_LEVEL_ENTITY [lindex $quartus(args) 3]

set_global_assignment -name SEARCH_PATH $search_path


# first check if there is a .qsf file for the specified board
# if so, source it
if { [file exists $board_qsf] } {
	source $board_qsf
	puts "Using $board_qsf"
} elseif { [file exists $family_qsf] } {
# if there is not a .qsf file for the board (or the board was not specified),
# check if there is a .qsf file for the device family.  If so, source it
	puts "Note: $board_qsf not found"
	source $family_qsf
	puts "Using $family_qsf"
} else {
# if neither a board or device .qsf file exists, print a warning
	puts "Warning: $board_qsf not found"
	puts "Warning: $family_qsf not found"
	puts "Using default Quartus device family"
}

# RCApprox setups
set_global_assignment -name EDA_DESIGN_ENTRY_SYNTHESIS_TOOL Synplify
set_global_assignment -name EDA_LMF_FILE synplcty.lmf -section_id eda_design_synthesis
set_global_assignment -name EDA_INPUT_DATA_FORMAT VQM -section_id eda_design_synthesis
set_global_assignment -name EDA_SIMULATION_TOOL "ModelSim (Verilog)"
set_global_assignment -name EDA_TIME_SCALE "1 ps" -section_id eda_simulation
set_global_assignment -name EDA_OUTPUT_DATA_FORMAT "VERILOG HDL" -section_id eda_simulation
set_global_assignment -name NUMBER_OF_REMOVED_REGISTERS_REPORTED 100000
set_global_assignment -name NUMBER_OF_SWEPT_NODES_REPORTED 100000
set_global_assignment -name NUMBER_OF_INVERTED_REGISTERS_REPORTED 100000
set_global_assignment -name SAVE_DISK_SPACE OFF
set_global_assignment -name OPTIMIZATION_TECHNIQUE AREA
set_global_assignment -name VERILOG_CONSTANT_LOOP_LIMIT 300000
set_global_assignment -name VERILOG_NON_CONSTANT_LOOP_LIMIT 300000

project_close


# Now that the project is closed, append "source common.qsf" to the file
set fo [open top.qsf a]
puts $fo "\n\nsource $common_qsf"


# EOF
