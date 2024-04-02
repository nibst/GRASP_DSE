#include "llvm/Support/CommandLine.h"
#include "llvm/Support/MathExtras.h"
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
#include "LegupConfig.h"
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <list>
#include <stdio.h>
#include <fstream>
#include <tuple>
#include <map>
#include "llvm/IR/DataLayout.h"

using namespace llvm;

//static cl::opt<std::string> OpIdCounter("ec", cl::desc("Specify the scheduling report file (.legup.rpt)"), cl::value_desc("envOpIdCounter"));
static cl::opt<std::string>	schedReportFileName("sr", cl::desc("Specify the scheduling report file (.legup.rpt)"), cl::value_desc("SchedulingReport"));
static cl::opt<std::string> configFileName("cf", cl::desc("Specify the device configuration file (.tcl)"), cl::value_desc("configFileName"));
static cl::opt<std::string> outputFileName("of", cl::desc("Specify output filename for updated instructions"), cl::value_desc("metadataFileName"));

namespace {
	struct ResourcesEvalPass : public ModulePass {
	    static char ID;
	    ResourcesEvalPass() : ModulePass(ID) {}

		// get operations states from legup's scheduling report
		std::map<uint64_t, std::string> getOpsState(std::string fileName){
			
			std::map<uint64_t, std::string> srOpState;
			std::ifstream srInputFile(fileName);
        	if(srInputFile.is_open()){
				char state[100];
				uint64_t opID;
				std::string line;
				while(getline(srInputFile, line)) { 
					if (line.find("state:", 0) != std::string::npos){
						sscanf(line.c_str(), "state: %99s", state);
						while(getline(srInputFile, line)){
							if (line.find("Transition:", 0) == std::string::npos) {
								sscanf(line.c_str(), "%lu", &opID);
								srOpState.insert(std::make_pair(opID, std::string(state)));
							}
							else {
								break;
							}
						}
			   		}
				}
				srInputFile.close();
				return srOpState;
			} else {
				errs() << "Failed to open " + fileName + '\n';
				exit(EXIT_FAILURE);
			}
		}
		
		// op name (format: F_BB_I)
		std::string getOpName(Instruction *I){
				
			std::string opName;
			if(I->hasName()){
				opName = I->getParent()->getParent()->getName().str() + "_" + I->getParent()->getName().str() + "_" + I->getName().str();  
				opName.erase(std::remove(opName.begin(), opName.end(), '.'), opName.end());
				opName.erase(std::remove(opName.begin(), opName.end(), '-'), opName.end());
			}
			else 
				opName = "";
			return opName;
		}

		std::list<Instruction*> getOpSources(Instruction *I){
			std::list<Instruction*> opSources;
			for (auto iterator = I->op_begin(); iterator != I->op_end(); ++iterator){
				if (auto source = dyn_cast<Instruction>(*iterator)){
					opSources.push_back(source);									
				}
			}
			return opSources;
		}

		std::list<Instruction*> getOpDestinations(Instruction *I){
			std::list<Instruction*> opDestinations;
			for(auto users : I->users()){  
				if (auto destination = dyn_cast<Instruction>(users)){
					opDestinations.push_back(destination);
				}
			}
			return opDestinations;
		}

		std::string getCSVStringFromOpList(std::list<Instruction*> opList){
			std::string opListCSVString;
			if (!opList.empty()){
				for (auto op : opList){
					MDNode* opIDNode = op->getMetadata("opID");
					if(opIDNode){
						opListCSVString += std::to_string(cast<ConstantInt>(opIDNode->getOperand(0))->getZExtValue()) + ",";
					}
				}
				opListCSVString.erase(opListCSVString.end() - 1);
				return opListCSVString;
			} else 
				return "";
		}

		std::tuple<int, int, int> getLegupResourcesUsage(Instruction *I){
			
			int luts, registers, dsps;
			int opCode = I->getOpcode();
			Type* opType = I->getType();
			DataLayout* dataLayout = new DataLayout(I->getParent()->getParent()->getParent()); 
			LegupConfig::LegupConfig *config = new LegupConfig::LegupConfig();
			LegupConfig::parseTclFile(configFileName, config);				
			if(LegupConfig::Operation* operation = config->getOpFromInst(I)){
				luts = operation->getLUTs();
				registers = operation->getRegisters(); 
				dsps = operation->getDSPElements();
			} else {
				luts = 0;
				registers = 0;                         
				dsps = 0;
			}
			// discard inputs registers 
			if(registers > 0){
				for (auto iterator = I->op_begin(); iterator != I->op_end(); ++iterator){
					registers -= (*iterator)->getType()->getScalarSizeInBits();									
				}
			} else if (opCode == Instruction::Load ||
						opCode == Instruction::GetElementPtr ||
						opCode ==  Instruction::PHI ||
						opCode ==  Instruction::Select){
				if(opType->isPtrOrPtrVectorTy())
					registers = dataLayout->getPointerTypeSizeInBits(opType);
				else
					registers = opType->getScalarSizeInBits();
			}
			return std::make_tuple(luts, registers, dsps);
		}

		std::string getOpState(uint64_t opID, std::map<uint64_t, std::string> srOpState){

			if(srOpState.find(opID) != srOpState.end())
				return srOpState[opID];
			else
				return "";
		}

		bool needsOutputRegisters(uint64_t opID, std::list<Instruction*> opDestinations, std::map<uint64_t, std::string> srOpState){
			
			bool needsRegisters = false;
			for (auto destination : opDestinations) {
				uint64_t destinationID = cast<ConstantInt>(destination->getMetadata("opID")->getOperand(0))->getZExtValue();
				int destOpCode = destination->getOpcode();
    			if(srOpState[destinationID] != srOpState[opID] || destOpCode == Instruction::PHI){
					needsRegisters = true;
					break;
				}
			}
			return needsRegisters;
		}

		virtual bool runOnModule(Module &M) {

			std::map<uint64_t, std::string> srOpState = getOpsState(schedReportFileName);

			FILE* outputFile = fopen(outputFileName.c_str(), "w");  
			for (auto &F : M){
		        for (auto &B : F) {
					for (auto &I : B) {
						
						uint64_t opID;
						StringRef opSignedness;

						if(I.hasMetadataOtherThanDebugLoc()){
							opID = cast<ConstantInt>(I.getMetadata("opID")->getOperand(0))->getZExtValue();
							opSignedness = cast<MDString>(I.getMetadata("opSignedness")->getOperand(0))->getString();
						} else {
							errs() << "Found instruction without metadata!";
							exit(EXIT_FAILURE);
						} 
						 
						// get operation name
						std::string opName = getOpName(&I);
						if(opName.empty())
							opName = "noname";
							
						// get sources string (CSV)
						std::list<Instruction*> opSources = getOpSources(&I); 
						std::string opSourcesCSVString = getCSVStringFromOpList(opSources);
						if(opSourcesCSVString.empty())
							opSourcesCSVString = "noopsources";
			
	             		// get destinations string (CSV)
						std::list<Instruction*> opDestinations = getOpDestinations(&I);
						std::string opDestinationsCSVString = getCSVStringFromOpList(opDestinations);
						if(opDestinationsCSVString.empty())
							opDestinationsCSVString = "noopdestinations";
						
						// get state name
						std::string opState = getOpState(opID, srOpState);
						if(opState.empty())
							opState = "nostate";
						
						// get default resources usage estimation from legup's characterization
						std::tuple<int, int, int> resources = getLegupResourcesUsage(&I);
						int luts = std::get<0>(resources);
						int registers = std::get<1>(resources);
						int dsps = std::get<2>(resources);
												
						// improve the resource usage estimation of constant-based operations
						if (I.isBinaryOp()){
							ConstantInt* constantValueLHS = dyn_cast<ConstantInt>(I.getOperand(0));
							ConstantInt* constantValueRHS = dyn_cast<ConstantInt>(I.getOperand(1));
							int opNumBits = I.getType()->getScalarSizeInBits();
							switch(I.getOpcode()){
								case Instruction::Shl:
								case Instruction::LShr:
									if(constantValueRHS){
										luts = 0;
										registers = opNumBits - constantValueRHS->getZExtValue();
										dsps = 0;
									}
									break;
								case Instruction::And:
									if(constantValueRHS){
										luts = 0;
										registers = constantValueRHS->getValue().getActiveBits();
										dsps = 0;
									}
									break;
								case Instruction::Or:
									if(constantValueRHS){
										luts = 0;
										registers = constantValueRHS->getValue().getBitWidth() - constantValueRHS->getValue().getActiveBits();
										dsps = 0;
									}
									break;
								case Instruction::Xor:	
								case Instruction::AShr:
									if(constantValueRHS){
										luts = 0;
										registers = opNumBits;
										dsps = 0;
									}
									break;
								case Instruction::Sub:	
								case Instruction::FSub:
									if (constantValueLHS){
										luts--;
									}
									else if (constantValueRHS) {
										luts -= constantValueRHS->getValue().countTrailingZeros();
									}
									break;
								case Instruction::Add:
								case Instruction::FAdd:
									if (constantValueRHS){
										luts -= constantValueRHS->getValue().countTrailingZeros();
									}
									break;
								case Instruction::Mul:
									if(constantValueRHS){
										uint64_t nextPowerOf2, previousPowerOf2, nearestPowerOf2, difference;
										APInt constantValue = constantValueRHS->getValue();
										if(constantValue.isNonNegative()){
											if(constantValue.isPowerOf2()){
												break;
											} else {
												uint64_t value = constantValue.getZExtValue();
												nextPowerOf2 = NextPowerOf2(value);
												previousPowerOf2 = PowerOf2Floor(value);
												nearestPowerOf2 = (nextPowerOf2 - value > value - previousPowerOf2) ? previousPowerOf2 : nextPowerOf2;
												difference = labs(value - nearestPowerOf2);
												if(isPowerOf2_64(difference)){
													luts = (value > nearestPowerOf2) ? (opNumBits - Log2_64(nearestPowerOf2)) : (opNumBits - Log2_64(difference));  
													registers = opNumBits - Log2_64(difference); 
													dsps = 0;
												}
											}
										} else { 
											uint64_t value = -constantValue.getSExtValue();
											if(isPowerOf2_64(value)){
												int logValue = Log2_64(value);
												luts = opNumBits - logValue - 1;
												registers = opNumBits - logValue;
												dsps = 0;
											}
										}
									} 		
									break;
			    				default:;
							}
		     			}
						
						if(I.getOpcode() != Instruction::PHI && !needsOutputRegisters(opID, opDestinations, srOpState))
						 	registers = 0;

						// write operation profile
						fprintf (outputFile, "ID:%lu|TYPE:%s|SIGN:%s|NAME:%s|STATE:%s|SOURCES:%s|DESTINATIONS:%s|LUTs:%i|REGs:%i|DSPs:%i|\n", opID, I.getOpcodeName(), opSignedness.data(), opName.c_str(), opState.c_str(), opSourcesCSVString.c_str(), opDestinationsCSVString.c_str(), luts, registers, dsps);
					}
				}
			}
			fclose(outputFile);
			return false;
		}
	};
}

char ResourcesEvalPass::ID = 0;
static RegisterPass<ResourcesEvalPass> X("resourcesEval", "ResourcesEval Pass");