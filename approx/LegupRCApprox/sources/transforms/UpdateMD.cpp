#include "llvm/Support/CommandLine.h"
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/Debug.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/IR/Metadata.h"
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <list>
#include <stdio.h>

using namespace llvm;

namespace {
	struct UpdateMDPass : public ModulePass {
	static char ID;
	UpdateMDPass() : ModulePass(ID) {}
   
	virtual bool runOnModule(Module &M) {
      
		LLVMContext &Ctx = M.getContext();
		std::list<uint64_t>::iterator opIDIterator;
		std::list<uint64_t> listOfOps;
		uint64_t opID, opIDCounter;
		
		// get the instruction counter value from the module metadata. If it's the first iteration, create the metadata						
		NamedMDNode* counterNamedMDNode = M.getOrInsertNamedMetadata("OP-ID-COUNTER");
		if(counterNamedMDNode->getNumOperands() != 0){
			opIDCounter = cast<ConstantInt>(counterNamedMDNode->getOperand(0)->getOperand(0))->getZExtValue();
			counterNamedMDNode->dropAllReferences();		
		}   	
		else
			opIDCounter = 0;

		bool MDUpdated = false;
		// iterates over all instructions to set metadata (unique dientifier and signedness) and names
		for (auto &F : M){
			for (auto &B : F){
				for (auto &I : B){
					if(MDNode* idMDNode = I.getMetadata("opID")){
						// instruction already has ID and signedness metadata (old instruction)     
						opID = cast<ConstantInt>(idMDNode->getOperand(0))->getZExtValue();
						opIDIterator = std::find(listOfOps.begin(), listOfOps.end(), opID);
						if(opIDIterator == listOfOps.end()){
							// instruction with unique ID 
							listOfOps.push_back(opID); 
						}
	                	else{ 
							// instruction with duplicated ID (cloned as a result of LLVM optimizations)
							I.setMetadata("opID", MDNode::get(Ctx, ConstantInt::get(Type::getInt64Ty(Ctx), ++opIDCounter)));
							if (!I.getType()->isVoidTy())
								I.setName(std::to_string(opIDCounter) + "." + I.getName().str()); 
							MDUpdated = true;
	                   	}
					}	   
					else{ 
						// new intruction not profiled yet 						
						I.setMetadata("opID", MDNode::get(Ctx, ConstantInt::get(Type::getInt64Ty(Ctx), ++opIDCounter)));
						if (!I.getType()->isVoidTy())
							I.setName(std::to_string(opIDCounter) + "." +I.getName().str()); 
						if(MDNode* signednessMDNode = I.getMetadata("opSignedness")){
							for(auto user : I.users()){  
								if (auto destination = dyn_cast<Instruction>(user)){
								    // destination instruction uses I 
									destination->setMetadata("opSignedness", signednessMDNode);
								}
							}
							for (auto operandIterator = I.op_begin(); operandIterator != I.op_end(); ++operandIterator){
			      				if (auto source = dyn_cast<Instruction>(*operandIterator)){
								 	// source instruction is used by I
	        						source->setMetadata("opSignedness", signednessMDNode);
								}
							}
						}
						// unknown signedness (at this point)
						else{
							I.setMetadata("opSignedness", MDNode::get(Ctx, MDString::get(Ctx, "unknownSignedness")));
						}
						MDUpdated = true;
            		}
            	}
			}
		}
		counterNamedMDNode->addOperand(MDNode::get(Ctx, ConstantInt::get(Type::getInt64Ty(Ctx), opIDCounter)));
		return MDUpdated;
	}
};
}

char UpdateMDPass::ID = 0;
static RegisterPass<UpdateMDPass> X("updateMD", "UpdateMD Pass");


