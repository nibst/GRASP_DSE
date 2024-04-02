add_llvm_loadable_module( LLVMRCApprox
	UpdateMD.cpp
	RemoveIOFCall.cpp
	Profiling.cpp
	Pruning.cpp
	ResourcesEval.cpp  
  )

target_link_libraries(LLVMRCApprox)
