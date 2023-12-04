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
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <list>
#include "llvm/IR/NoFolder.h"

using namespace llvm;

static cl::opt<std::string> outputFileName("pf", cl::desc("Specify output filename for profiling results"), cl::value_desc("filename"));

namespace {
  struct ProfilingPass : public ModulePass {
    static char ID;
    ProfilingPass() : ModulePass(ID) {}
    
    virtual bool runOnModule(Module &M) {
      LLVMContext &Ctx = M.getContext();
      
      Type* retType = Type::getVoidTy(Ctx);
      std::vector<Type*> paramTypes = {Type::getInt64Ty(Ctx), Type::getInt8Ty(Ctx), Type::getInt64Ty(Ctx), Type::getInt64Ty(Ctx), 
                                       Type::getDoubleTy(Ctx), Type::getInt1Ty(Ctx), Type::getInt1Ty(Ctx), Type::getInt32Ty(Ctx)};
      std::vector<Type*> paramTypeFileName = {Type::getInt8PtrTy(Ctx)};
      Constant *profOp = M.getOrInsertFunction("profOp", FunctionType::get(retType, paramTypes, false));
      Constant *saveProfile = M.getOrInsertFunction("saveProfile", FunctionType::get(retType, paramTypeFileName, false));
      
      GlobalVariable* fileNameString = new GlobalVariable(M, ArrayType::get(Type::getInt8Ty(Ctx), outputFileName.length() + 1), 
                                                          true, GlobalValue::PrivateLinkage, 
                                                          ConstantDataArray::getString(Ctx, outputFileName, true), "filename");
      Constant *zero = ConstantInt::get(Type::getInt32Ty(Ctx), 0);
      Constant *index[] = { zero, zero };
      Constant *fileNameRef = ConstantExpr::getInBoundsGetElementPtr(fileNameString->getValueType(),fileNameString, index);  

      bool profiled = false;
      Value* args[8];                
      for (auto &F : M){
        for (auto &B : F) {
          for (auto &I : B) { 
            if(I.isBinaryOp() && I.hasMetadataOtherThanDebugLoc()){ 
            	  // Insert *after* `op`.
                IRBuilder<NoFolder> builder(&I);
            	  builder.SetInsertPoint(&B, ++builder.GetInsertPoint());
            	  // Insert a call to the profiling function. 
                MDNode* idMDNode = I.getMetadata("opID");
                ConstantInt *opID;
                if (MDNode* N = I.getMetadata("stats.instNumber")) {
                  const char* string = cast<MDString>(N->getOperand(0))->getString().data();
                  fprintf(stderr,"%s",string);
                  opID = ConstantInt::get(Type::getInt64Ty(Ctx), std::stoi(string));
                }
                ConstantInt *opCode = ConstantInt::get(Type::getInt8Ty(Ctx), I.getOpcode()); 
                StringRef opSignedness = cast<MDString>(I.getMetadata("opSignedness")->getOperand(0))->getString();
  
                //algum erro no switch, alem de ter erro no opID e opCode que comentei         	                
                switch(I.getOpcode()){
                  case Instruction::FAdd:
                  case Instruction::FSub:
                  case Instruction::FMul:
                  case Instruction::FDiv:
                  case Instruction::FRem:
                          args[0] = opID; 
                          fprintf(stderr,"0");  
                          args[1] = opCode; 
                          fprintf(stderr,"1");  
                          args[2] = ConstantInt::get(Type::getInt64Ty(Ctx), 0); 
                          fprintf(stderr,"2");  
                          args[3] = ConstantInt::get(Type::getInt64Ty(Ctx), 0); 
                          fprintf(stderr,"3");
                          args[4] = builder.CreateFPExt(&I, Type::getDoubleTy(Ctx)); 
                          fprintf(stderr,"4");
                          args[5] = ConstantInt::get(Type::getInt1Ty(Ctx), 0); 
                          fprintf(stderr,"5");
                          args[6] = ConstantInt::get(Type::getInt1Ty(Ctx), 1);
                          fprintf(stderr,"6");
                          args[7] = ConstantInt::get(Type::getInt32Ty(Ctx), I.getType()->getPrimitiveSizeInBits());
               		        fprintf(stderr,"7");
                          builder.CreateCall(profOp, args);
                          fprintf(stderr,"builder");
                          profiled = true;
                          break;
                  case Instruction::Add:
                  case Instruction::Sub:
                  case Instruction::Mul:
                  case Instruction::Or:
                  case Instruction::And:
                  case Instruction::Xor:
                  case Instruction::Shl:
                  case Instruction::LShr:
                  case Instruction::AShr:
                          if(opSignedness == "unsigned"){
                              args[0] = opID; 
                              fprintf(stderr,"0 uns");
                              args[1] = opCode; 
                              fprintf(stderr,"1 uns");
                              args[2] = ConstantInt::get(Type::getInt64Ty(Ctx), 0);
                              fprintf(stderr,"2 uns");
                              args[3] = builder.CreateZExt(&I, Type::getInt64Ty(Ctx)); 
                              fprintf(stderr,"3 uns");
                              args[4] = ConstantFP::get(Type::getDoubleTy(Ctx), 0); 
                              fprintf(stderr,"4 uns");
                              args[5] = ConstantInt::get(Type::getInt1Ty(Ctx), 0); 
                              fprintf(stderr,"2 uns");
                              args[6] = ConstantInt::get(Type::getInt1Ty(Ctx), 0);
                              fprintf(stderr,"2 uns");
                              args[7] = ConstantInt::get(Type::getInt32Ty(Ctx), I.getType()->getPrimitiveSizeInBits());
                              fprintf(stderr,"2 uns");
                              builder.CreateCall(profOp, args);
                              profiled = true;
                          }
                          else { 
                            if((opSignedness == "signed") || (opSignedness == "unknownSignedness")){//assume signed?
                              args[0] = opID; 
                              args[1] = opCode; 
                              args[2] = builder.CreateSExt(&I, Type::getInt64Ty(Ctx)); 
                              args[3] = ConstantInt::get(Type::getInt64Ty(Ctx), 0);
                              args[4] = ConstantFP::get(Type::getDoubleTy(Ctx), 0); 
                              args[5] = ConstantInt::get(Type::getInt1Ty(Ctx), 1); 
                              args[6] = ConstantInt::get(Type::getInt1Ty(Ctx), 0);
                              args[7] = ConstantInt::get(Type::getInt32Ty(Ctx), I.getType()->getPrimitiveSizeInBits());
                              builder.SetInsertPoint(&B, builder.GetInsertPoint());
                              builder.CreateCall(profOp, args);
                              profiled = true;
                            }
                          }
			                    break;
		              case Instruction::UDiv:
                  case Instruction::URem:
                          args[0] = opID; 
                          fprintf(stderr,"0");
                          args[1] = opCode; 
                          fprintf(stderr,"0");
                          args[2] = ConstantInt::get(Type::getInt64Ty(Ctx), 0);
                          fprintf(stderr,"2");
                          args[3] = builder.CreateZExt(&I, Type::getInt64Ty(Ctx)); 
                          fprintf(stderr,"3");
                          args[4] = ConstantFP::get(Type::getDoubleTy(Ctx), 0); 
                          fprintf(stderr,"4");
                          args[5] = ConstantInt::get(Type::getInt1Ty(Ctx), 0); 
                          fprintf(stderr,"5");
                          args[6] = ConstantInt::get(Type::getInt1Ty(Ctx), 0);
                          fprintf(stderr,"6");
                          args[7] = ConstantInt::get(Type::getInt32Ty(Ctx), I.getType()->getPrimitiveSizeInBits());
                          fprintf(stderr,"7");
                          builder.CreateCall(profOp, args);
                          fprintf(stderr,"udiv builkd");
                          profiled = true;
                          break;
                  case Instruction::SDiv:
                  case Instruction::SRem:
                          args[0] = opID; 
                          fprintf(stderr,"0 srem");
                          args[1] = opCode; 
                          fprintf(stderr,"1 srem");
                          args[2] = builder.CreateSExt(&I, Type::getInt64Ty(Ctx)); 
                          fprintf(stderr,"2 srem");
                          args[3] = ConstantInt::get(Type::getInt64Ty(Ctx), 0);
                          fprintf(stderr,"3 srem");
                          args[4] = ConstantFP::get(Type::getDoubleTy(Ctx), 0); 
                          fprintf(stderr,"4 srem");
                          args[5] = ConstantInt::get(Type::getInt1Ty(Ctx), 1); 
                          fprintf(stderr,"5 srem");
                          args[6] = ConstantInt::get(Type::getInt1Ty(Ctx), 0);
                          fprintf(stderr,"6 srem");
                          args[7] = ConstantInt::get(Type::getInt32Ty(Ctx), I.getType()->getPrimitiveSizeInBits());
                          fprintf(stderr,"7 srem");
                          builder.CreateCall(profOp, args);
                          fprintf(stderr,"build SREM");
                          profiled = true;
                	        break;
                  default:;
                      // load, store, phi, getelementptr (index and pointer arithmetic)      
                }
                
            }
            else { 
              if(auto *op = dyn_cast<ReturnInst>(&I)){
                if(F.getName() == "main" && profiled){
                  fprintf(stderr,"else");
          	      IRBuilder<> builder(op);
                  builder.SetInsertPoint(&B, builder.GetInsertPoint());
                  builder.CreateCall(saveProfile, fileNameRef);
                } 
              }
            } 
          }
        }
      }
      return profiled;
    }
  };
}

char ProfilingPass::ID = 0;
static RegisterPass<ProfilingPass> X("profiling", "Profiling Pass");

// Automatically enable the pass.
// http://adriansampson.net/blog/clangpass.html
//static void registerSkeletonPass(const PassManagerBuilder &,
//                         legacy::PassManagerBase &PM) {
//  PM.add(new SkeletonPass());
//}
//static RegisterStandardPasses
//  RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
//                 registerSkeletonPass);
