#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Instructions.h"
#include "llvm/ADT/StringExtras.h"
#include <string>
#include <set>
#include <map>

using namespace llvm;

namespace LegupConfig {

class Operation {
public:
  Operation() {}

  Operation(float FMax, float CritDelay, float StaticPower, float DynamicPower,
            int LUTs, int Registers, int LogicElements, int DSPElements,
            int Latency)
      : FMax(FMax), CritDelay(CritDelay), StaticPower(StaticPower),
        DynamicPower(DynamicPower), LUTs(LUTs), Registers(Registers),
        LogicElements(LogicElements), DSPElements(DSPElements),
        Latency(Latency) {}

  float getFmax() { return FMax; }
  float getCritDelay() { return CritDelay; }
  float getStaticPower() { return StaticPower; }
  float getDynamicPower() { return DynamicPower; }
  int getLUTs() { return LUTs; }
  int getRegisters() { return Registers; }
  int getLogicElements() { return LogicElements; }
  int getDSPElements() { return DSPElements; }
  int getLatency() { return Latency; }

private:
  float FMax;
  float CritDelay;
  float StaticPower;
  float DynamicPower;
  int LUTs;
  int Registers;
  int LogicElements;
  int DSPElements;
  int Latency;
};

class LegupConfig {
public:
  LegupConfig() : maxLatency(0), clkPeriod(0) {}
  
  ~LegupConfig() {
    for (std::map<std::pair<std::string, int>, Operation *>::iterator i = Operations.begin(), 
		e = Operations.end(); i != e; ++i) {
      assert(i->second);
      delete i->second;
    }
  }
  void setClkPeriod(const int clkPeriod) { this->clkPeriod = clkPeriod; }
  void addOperation(const std::string op_name, const float FMax,
                    const float CritDelay, const float StaticPower,
                    const float DynamicPower, const int LUTs,
                    const int Registers, const int LogicElements,
                    const int DSPElements, const int Latency) {
    Operations[std::make_pair(op_name, Latency)] =
        new Operation(FMax, CritDelay, StaticPower, DynamicPower, LUTs,
                      Registers, LogicElements, DSPElements, Latency);
    if (Latency > maxLatency)
      maxLatency = Latency;
  }
 
  Operation *getOpFromInst(Instruction *instr) {
    return getOperationRef(getOpNameFromInst(instr));
  }

private:
    
  std::map<std::pair<std::string, int>, Operation *> Operations;
  int maxLatency;
  int clkPeriod;
  
  std::string getOpNameFromInst(Instruction *instr);
  bool isAnyOfTwoOperandsZero(Instruction *instr);
  bool populateStringsForOneOperandInstr(Instruction *instr, std::string params[10]);
  bool populateStringsForTwoOperandInstr(Instruction *instr, std::string params[10]);
  bool populateStringsForThreeOperandInstr(Instruction *instr, std::string params[10]);
  bool populateStringsForBinaryOperator(Instruction *instr, std::string params[10]);
  void populateStringsForICmpInst(const ICmpInst *cmp, std::string params[10]);
  void populateStringsForFCmpInst(const FCmpInst *cmp, std::string params[10]);
  bool isBinaryOperatorNoOp(Instruction *instr);
  bool isSecondOperandZero(Instruction *instr);
  bool isSecondOperandPowerOfTwo(Instruction *instr);
  bool isSecondOperandConstant(Instruction *instr);
  int maxBitWidth(int width0, int width1, int width2);
  bool isSupportedBitwidth(int width);
  std::string assembleOpNameFromStringList(std::string params[10]);
  
  bool check_op_exists(const std::string op_name, int &latency) {
   
    int i;
    for (i = 0; i <= maxLatency; i++) {
      if (Operations.find(std::make_pair(op_name, i)) != Operations.end()) {
        latency = i; 
        return true;
      }
    }
    return false;
  }

  Operation *getOperationRef(const std::string op_name) {
    int latency;
    if(check_op_exists(op_name, latency)){
    	const std::pair<std::string, int> op = std::make_pair(op_name, latency); 
    	return Operations[op];
    }
    return nullptr;
  }

 
};

bool parseTclFile(std::string &ConfigFile, LegupConfig *legupConfig);

}

