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

	virtual bool runOnModule(Module &module) {
      
		LLVMContext &Ctx = module.getContext();
		std::list<uint64_t>::iterator opIDIterator;
		std::list<uint64_t> listOfOps;
		uint64_t opID, opIDCounter;
		Type* retType = Type::getVoidTy(Ctx);
		std::vector<Type*> paramTypes = {Type::getInt64Ty(Ctx)};
		std::vector<Type*> paramTypeFileName = {Type::getInt8PtrTy(Ctx)};
		// get the instruction counter value from the module metadata. If it's the first iteration, create the metadata						
		NamedMDNode* counterNamedMDNode = module.getOrInsertNamedMetadata("OP-ID-COUNTER");
		if(counterNamedMDNode->getNumOperands() != 0){
			opIDCounter = cast<ConstantInt>(dyn_cast<ConstantAsMetadata>(counterNamedMDNode->getOperand(0)->getOperand(0))->getValue())->getZExtValue();
			counterNamedMDNode->dropAllReferences();		
		}   	
		else
			opIDCounter = 0;
		bool MDUpdated = false;
		// iterates over all instructions to set metadata (unique dientifier and signedness) and names
		for (auto &func : module){
			for (auto &basicBlock : func){
				for (auto &instruction : basicBlock){
					if(MDNode* idMDNode = instruction.getMetadata("opID")){
						// instruction already has ID and signedness metadata (old instruction)   
						opID = cast<ConstantInt>(dyn_cast<ConstantAsMetadata>(dyn_cast<MDNode>(idMDNode->getOperand(0))->getOperand(0))->getValue())->getZExtValue();
						opIDIterator = std::find(listOfOps.begin(), listOfOps.end(), opID);
						//if opID not found:
						if(opIDIterator == listOfOps.end()){
							// instruction with unique ID 
							listOfOps.push_back(opID); 
						}
	                	else{ 
							
							// instruction with duplicated ID (cloned as a result of LLVM optimizations)
							instruction.setMetadata("opID", MDNode::get(Ctx, ConstantAsMetadata::get(ConstantInt::get(Type::getInt64Ty(Ctx), ++opIDCounter))));
							MDNode* N = MDNode::get(Ctx, MDString::get(Ctx, std::to_string(opIDCounter)));
         					instruction.setMetadata("stats.instNumber", N);
							if (!instruction.getType()->isVoidTy())
								instruction.setName(std::to_string(opIDCounter) + "." + instruction.getName().str()); 
							MDUpdated = true;
	                   	}
					}	   
					else{ 

						// new intruction not profiled yet 						
						instruction.setMetadata("opID", MDNode::get(Ctx, ConstantAsMetadata::get(ConstantInt::get(Type::getInt64Ty(Ctx), ++opIDCounter))));
						MDNode* N = MDNode::get(Ctx, MDString::get(Ctx, std::to_string(opIDCounter)));
         				instruction.setMetadata("stats.instNumber", N);
						if (!instruction.getType()->isVoidTy())
							instruction.setName(std::to_string(opIDCounter) + "." +instruction.getName().str()); 
						if(MDNode* signednessMDNode = instruction.getMetadata("opSignedness")){
							for(auto user : instruction.users()){  
								if (auto destination = dyn_cast<Instruction>(user)){
								    // destination(instruction) uses instruction 
									destination->setMetadata("opSignedness", signednessMDNode);
								}
							}
							for (auto operandIterator = instruction.op_begin(); operandIterator != instruction.op_end(); ++operandIterator){
			      				if (auto source = dyn_cast<Instruction>(*operandIterator)){
								 	// source(instruction) is used by instruction
	        						source->setMetadata("opSignedness", signednessMDNode);
								}
							}
						}
						// unknown signedness (at this point)
						else{
							instruction.setMetadata("opSignedness", MDNode::get(Ctx, MDString::get(Ctx, "unknownSignedness")));
						}
						MDUpdated = true;
            		}
            	}
			}
		}
		counterNamedMDNode->addOperand(MDNode::get(Ctx, ConstantAsMetadata::get(ConstantInt::get(Type::getInt64Ty(Ctx), opIDCounter))));
		return MDUpdated;
	}
};
}

char UpdateMDPass::ID = 0;
static RegisterPass<UpdateMDPass> X("updateMD", "UpdateMD Pass");


