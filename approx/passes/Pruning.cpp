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
#include "llvm/Analysis/CallGraph.h"
#include "llvm/Analysis/TargetLibraryInfo.h"

using namespace llvm;

static cl::opt<std::string> opToPrune("opID", cl::desc("Specify the ID of the operation to be pruned."), cl::value_desc("operationID"));
static cl::opt<std::string> opValue("opValue", cl::desc("Specify the constant value to replace the operation."), cl::value_desc("operationValue"));

namespace
{
   struct PruningPass : public ModulePass
   {
      static char ID;
      PruningPass() : ModulePass(ID) {}

      virtual bool runOnModule(Module &M)
      {
         uint64_t opIdU64 = strtoul((opToPrune).c_str(), NULL, 0);
         double opValDouble = strtod((opValue).c_str(), NULL);
         bool pruned = false;
         for (auto &F : M){
            for (auto &B : F){
               for (BasicBlock::iterator I = B.begin(), E = B.end(); I != E;){
                  Instruction *op = &*I;
                  ++I;
                  if (op->isBinaryOp())
                     if(auto opID = op->getMetadata("opID"))
                        if(cast<ConstantInt>(dyn_cast<ConstantAsMetadata>(dyn_cast<MDNode>(opID->getOperand(0))->getOperand(0))->getValue())->getZExtValue() == opIdU64){
                           BasicBlock::iterator iter(op);
                           pruned = true;
                           if (op->getType()->isFloatingPointTy())
                              ReplaceInstWithValue(op->getParent()->getInstList(), iter, ConstantFP::get(op->getType(), opValDouble));
                           else if (op->getType()->isIntegerTy())
                              ReplaceInstWithValue(op->getParent()->getInstList(), iter, ConstantInt::get(op->getType(), opValDouble));
                           else
                              pruned = false;
                        }
                  if (pruned)
                     break;
               }
            }
         }
         return pruned;
      }
   };
}

char PruningPass::ID = 0;
static RegisterPass<PruningPass> X("pruning", "Pruning Pass");
