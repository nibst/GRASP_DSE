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

using namespace llvm;

namespace {
  struct RemoveIOFCallPass : public ModulePass {
    static char ID;
    RemoveIOFCallPass() : ModulePass(ID) {}
    
    virtual bool runOnModule(Module &M) {
      bool removed = false;  
      for (auto &F : M){
       for (auto &B : F) {
         for (BasicBlock::iterator I = B.begin(), E = B.end(); I != E;) { 
            Instruction *op = &*I;
            ++I;
            if(auto *call = dyn_cast<CallInst>(op)){
               Function* calledFunction = call->getCalledFunction();
               StringRef functionName = calledFunction->getName();
               if(functionName == "populateInput" || functionName == "populateOutput"){
                   call->eraseFromParent();
                   calledFunction->eraseFromParent();
                   removed = true;
              }
            }
           
        }
       }
      }
      return removed;
    }
  };
}

char RemoveIOFCallPass::ID = 0;
static RegisterPass<RemoveIOFCallPass> X("removeIOFCall", "RemoveIOFCall Pass");



