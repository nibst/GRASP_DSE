set moduleName sha_transform
set isTopModule 0
set isTaskLevelControl 1
set isCombinational 0
set isDatapathOnly 0
set isFreeRunPipelineModule 0
set isPipelined 0
set pipeline_type none
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set C_modelName {sha_transform}
set C_modelType { void 0 }
set C_modelArgList {
	{ sha_info_data int 32 regular {array 16 { 1 3 } 1 1 } {global 0}  }
	{ sha_info_digest int 32 regular {array 5 { 2 2 } 1 1 } {global 2}  }
}
set C_modelArgMapList {[ 
	{ "Name" : "sha_info_data", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY", "bitSlice":[{"low":0,"up":31,"cElement": [{"cName": "sha_info_data","cData": "unsigned int","bit_use": { "low": 0,"up": 31},"cArray": [{"low" : 0,"up" : 15,"step" : 1}]}]}], "extern" : 0} , 
 	{ "Name" : "sha_info_digest", "interface" : "memory", "bitwidth" : 32, "direction" : "READWRITE", "bitSlice":[{"low":0,"up":31,"cElement": [{"cName": "sha_info_digest","cData": "unsigned int","bit_use": { "low": 0,"up": 31},"cArray": [{"low" : 0,"up" : 4,"step" : 1}]}]}], "extern" : 0} ]}
# RTL Port declarations: 
set portNum 19
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ sha_info_data_address0 sc_out sc_lv 4 signal 0 } 
	{ sha_info_data_ce0 sc_out sc_logic 1 signal 0 } 
	{ sha_info_data_q0 sc_in sc_lv 32 signal 0 } 
	{ sha_info_digest_address0 sc_out sc_lv 3 signal 1 } 
	{ sha_info_digest_ce0 sc_out sc_logic 1 signal 1 } 
	{ sha_info_digest_we0 sc_out sc_logic 1 signal 1 } 
	{ sha_info_digest_d0 sc_out sc_lv 32 signal 1 } 
	{ sha_info_digest_q0 sc_in sc_lv 32 signal 1 } 
	{ sha_info_digest_address1 sc_out sc_lv 3 signal 1 } 
	{ sha_info_digest_ce1 sc_out sc_logic 1 signal 1 } 
	{ sha_info_digest_we1 sc_out sc_logic 1 signal 1 } 
	{ sha_info_digest_d1 sc_out sc_lv 32 signal 1 } 
	{ sha_info_digest_q1 sc_in sc_lv 32 signal 1 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "sha_info_data_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "sha_info_data", "role": "address0" }} , 
 	{ "name": "sha_info_data_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "sha_info_data", "role": "ce0" }} , 
 	{ "name": "sha_info_data_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "sha_info_data", "role": "q0" }} , 
 	{ "name": "sha_info_digest_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "address0" }} , 
 	{ "name": "sha_info_digest_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "ce0" }} , 
 	{ "name": "sha_info_digest_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "we0" }} , 
 	{ "name": "sha_info_digest_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "d0" }} , 
 	{ "name": "sha_info_digest_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "q0" }} , 
 	{ "name": "sha_info_digest_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "address1" }} , 
 	{ "name": "sha_info_digest_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "ce1" }} , 
 	{ "name": "sha_info_digest_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "we1" }} , 
 	{ "name": "sha_info_digest_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "d1" }} , 
 	{ "name": "sha_info_digest_q1", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "sha_info_digest", "role": "q1" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1"],
		"CDFG" : "sha_transform",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "395", "EstimateLatencyMax" : "395",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "sha_info_data", "Type" : "Memory", "Direction" : "I"},
			{"Name" : "sha_info_digest", "Type" : "Memory", "Direction" : "IO"}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.W_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	sha_transform {
		sha_info_data {Type I LastRead 1 FirstWrite -1}
		sha_info_digest {Type IO LastRead 5 FirstWrite 9}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "395", "Max" : "395"}
	, {"Name" : "Interval", "Min" : "395", "Max" : "395"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	sha_info_data { ap_memory {  { sha_info_data_address0 mem_address 1 4 }  { sha_info_data_ce0 mem_ce 1 1 }  { sha_info_data_q0 mem_dout 0 32 } } }
	sha_info_digest { ap_memory {  { sha_info_digest_address0 mem_address 1 3 }  { sha_info_digest_ce0 mem_ce 1 1 }  { sha_info_digest_we0 mem_we 1 1 }  { sha_info_digest_d0 mem_din 1 32 }  { sha_info_digest_q0 mem_dout 0 32 }  { sha_info_digest_address1 MemPortADDR2 1 3 }  { sha_info_digest_ce1 MemPortCE2 1 1 }  { sha_info_digest_we1 MemPortWE2 1 1 }  { sha_info_digest_d1 MemPortDIN2 1 32 }  { sha_info_digest_q1 MemPortDOUT2 0 32 } } }
}
