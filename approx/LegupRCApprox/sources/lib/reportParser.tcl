load_package report
project_open top
load_report

set panel {Fitter||Resource Section||Fitter Resource Usage Summary}
set id [get_report_panel_id $panel]

set logicLUTs [string map {, ""} [get_report_panel_data -row_name "Combinational ALUT usage for logic" -col_name "Usage" -id $id]]
set routeLUTs [string map {, ""} [get_report_panel_data -row_name "Combinational ALUT usage for route-throughs" -col_name "Usage" -id $id]]
set LUTs [expr {$logicLUTs + $routeLUTs}]
set REGs [string map {, ""} [get_report_panel_data -row_name "Dedicated logic registers" -col_name "Usage" -id $id]]
set DSPs [string map {, ""} [get_report_panel_data -row_name "Total DSP Blocks" -col_name "Usage" -id $id]]
set DSPs [split $DSPs " "]
set DSPs [lindex $DSPs 0]

set metricsOutputFile [open "resourcesUsage.txt" "w"]
puts $metricsOutputFile "LUTs: $LUTs\nREGs: $REGs\nDSPs: $DSPs"
close $metricsOutputFile

set panel {Analysis & Synthesis||Analysis & Synthesis Optimization Results||Register Statistics||Registers Removed During Synthesis}
set id [get_report_panel_id $panel]
set num_rows [get_number_of_rows -id $id]

set mergedRegsOutputFile [open "mergedRegs.txt" "w"]
set removedRegsOutputFile [open "removedRegs.txt" "w"]

for { set i 1 } { $i < $num_rows - 1 } { incr i } {
 	set register_removed [get_report_panel_data -row $i -col 0 -id $id]
	set reason [get_report_panel_data -row $i -col 1 -id $id] 	
	regsub -all {[^|]+:} $register_removed "" register_removed	
	if { [ regexp {^Merged with\s+(.+)$} $reason reason register_shared ] } {
		regsub -all {[^|]+:} $register_shared "" register_shared		
		if { [ regexp {^.+\[(\d+)\.\.(\d+)\]$} $register_removed match low_reg high_reg ] } {
			for { set j $low_reg } { $j <= $high_reg } { incr j } {
				regsub {\[.+\]} $match "\[$j\]" register_removed_single
				puts $mergedRegsOutputFile "\\$register_removed_single:\\$register_shared" 
			}
		} elseif { [ regexp {^.+\[([\d\.]+\,.+)\]$} $register_removed match regs ] } {
				set regs_list [split $regs ","]
				foreach reg $regs_list {
					if { [ regexp {^(\d+)\.\.(\d+)$} $reg range_match low_reg high_reg ] } {					
						for { set j $low_reg } { $j <= $high_reg } { incr j } {
							regsub {\[.+\]} $match "\[$j\]" register_removed_single
							puts $mergedRegsOutputFile "\\$register_removed_single:\\$register_shared" 
						}
						 					
					} else {
						regsub {\[.+\]} $match "\[$reg\]" register_removed_single
						puts $mergedRegsOutputFile "\\$register_removed_single:\\$register_shared"
					}				
				} 

		} else {
			puts $mergedRegsOutputFile "\\$register_removed:\\$register_shared"
		} 

	} elseif { [ regexp {^.+\[(\d+)\.\.(\d+)\]$} $register_removed match low_reg high_reg ] } {
		for { set j $low_reg } { $j <= $high_reg } { incr j } {
			regsub {\[.+\]} $match "\[$j\]" register_removed_single
			puts $removedRegsOutputFile "\\$register_removed_single" 
		}
	} elseif { [ regexp {^.+\[([\d\.]+\,.+)\]$} $register_removed match regs ] } {
			set regs_list [split $regs ","]
			foreach reg $regs_list {
				if { [ regexp {^(\d+)\.\.(\d+)$} $reg range_match low_reg high_reg ] } {					
					for { set j $low_reg } { $j <= $high_reg } { incr j } {
						regsub {\[.+\]} $match "\[$j\]" register_removed_single
						puts $removedRegsOutputFile "\\$register_removed_single" 
					}
				} else {
					regsub {\[.+\]} $match "\[$reg\]" register_removed_single
					puts $removedRegsOutputFile "\\$register_removed_single"
				}				
			} 
	} else {
		puts $removedRegsOutputFile "\\$register_removed"
	} 			

}
close $mergedRegsOutputFile	
close $removedRegsOutputFile	

set panel {Fitter||Fitter Netlist Optimizations}
set id [get_report_panel_id $panel]
set num_rows [get_number_of_rows -id $id]

set packedRegsOutputFile [open "packedRegs.txt" "w"]
set duplicatedRegsOutputFile [open "duplicatedRegs.txt" "w"]

for { set i 0 } { $i < $num_rows } { incr i } {
	set action [get_report_panel_data -row $i -col 1 -id $id]
	if { [string equal $action "Packed Register"] } {
		set node [get_report_panel_data -row $i -col 0 -id $id]
		regsub -all {[^|]+:} $node "" node
		set destination [get_report_panel_data -row $i -col 6 -id $id]
		regsub -all {[^|]+:} $destination "" destination 
		puts $packedRegsOutputFile "\\$node:\\$destination"	
	} elseif { [string equal $action "Duplicated"] } {
		set node [get_report_panel_data -row $i -col 0 -id $id]
		regsub -all {[^|]+:} $node "" node
		set copy [get_report_panel_data -row $i -col 6 -id $id]
		regsub -all {[^|]+:} $copy "" copy 
		puts $duplicatedRegsOutputFile "\\$node:\\$copy"	
	}
}	
close $packedRegsOutputFile
close $duplicatedRegsOutputFile


