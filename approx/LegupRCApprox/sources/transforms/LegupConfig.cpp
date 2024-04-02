#ifndef USE_INTERP_RESULT
#define USE_INTERP_RESULT
#endif

#ifndef USE_INTERP_ERRORLINE
#define USE_INTERP_ERRORLINE
#endif

#include "LegupConfig.h"
#include <tcl/tcl.h>
#include <sstream>

using namespace llvm;

namespace LegupConfig {

bool LegupConfig::isAnyOfTwoOperandsZero(Instruction *instr) {
    for (int i = 0; i < 2; i++) {
        ConstantInt *ci = dyn_cast<ConstantInt>(instr->getOperand(i));
        if (ci && ci->isZero()) {
            return true;
        }
    }
    return false;
}

bool LegupConfig::isSecondOperandZero(Instruction *instr) {
    ConstantInt *ci = dyn_cast<ConstantInt>(instr->getOperand(1));
    return ci && ci->isZero();
}

bool LegupConfig::isSecondOperandPowerOfTwo(Instruction *instr) {
    ConstantInt *ci = dyn_cast<ConstantInt>(instr->getOperand(1));
    return ci && ci->getValue().isPowerOf2();
}

bool LegupConfig::isSecondOperandConstant(Instruction *instr) {
    return isa<ConstantInt>(instr->getOperand(1));
}

int LegupConfig::maxBitWidth(int width0, int width1, int width2) {
    return (width0 >= width1) ? (width0 >= width2) ? width0 : width2
                              : (width1 >= width2) ? width1 : width2;
}

bool LegupConfig::isSupportedBitwidth(int width) {
    return width == 8 || width == 16 || width == 32 || width == 64;
}

bool LegupConfig::isBinaryOperatorNoOp(Instruction *instr) {
    switch (instr->getOpcode()) {
    case Instruction::Add:
        // x + 0 = 0 + x = x
        if (isAnyOfTwoOperandsZero(instr))
            return true;
        break;
    case Instruction::Sub:
        // x - 0 = x
        if (isSecondOperandZero(instr))
            return true;
        break;
    case Instruction::Mul:
    case Instruction::URem:
    case Instruction::UDiv:
        if (isSecondOperandPowerOfTwo(instr))
            return true;
        break;
    case Instruction::And:
    case Instruction::Or:
    case Instruction::Shl:
    case Instruction::AShr:
    case Instruction::LShr:
        if (isSecondOperandConstant(instr)) {
            // If the second operand is a constant
            return true;
        }
        break;
    }
    return false;
}

bool LegupConfig::populateStringsForBinaryOperator(Instruction *instr,
                                                   std::string params[10]) {
    switch (instr->getOpcode()) {
    case Instruction::Add:
        params[0] = "signed";
        params[1] = "add";
        break;
    case Instruction::FAdd:
        params[0] = "altfp";
        params[1] = "add";
        break;
    case Instruction::FMul:
        params[0] = "altfp";
        params[1] = "multiply";
        break;
    case Instruction::FSub:
        params[0] = "altfp";
        params[1] = "subtract";
        break;
    case Instruction::FDiv:
        params[0] = "altfp";
        params[1] = "divide";
        break;
    case Instruction::Sub:
        params[0] = "signed";
        params[1] = "subtract";
        break;
    case Instruction::Mul:
        params[0] = "signed";
        params[1] = "multiply";
        break;
    case Instruction::URem:
        params[0] = "unsigned";
        params[1] = "modulus";
        break;
    case Instruction::UDiv:
        params[0] = "unsigned";
        params[1] = "divide";
        break;
    case Instruction::And:
        params[0] = "bitwise";
        params[1] = "AND";
        break;
    case Instruction::Or:
        params[0] = "bitwise";
        params[1] = "OR";
        break;
    case Instruction::Xor:
        params[0] = "bitwise";
        params[1] = "XOR";
        break;
    case Instruction::Shl:
        params[0] = "shift";
        params[1] = "ll";
        break;
    case Instruction::AShr:
        params[0] = "shift";
        params[1] = "ra";
        break;
    case Instruction::LShr:
        params[0] = "shift";
        params[1] = "rl";
        break;
    case Instruction::SRem:
        params[0] = "signed";
        params[1] = "modulus";
        break;
    case Instruction::SDiv:
        params[0] = "signed";
        params[1] = "divide";
        break;
    default:
        errs() << "Invalid operator type!\n";
    }
    return !isBinaryOperatorNoOp(instr);
}

void LegupConfig::populateStringsForICmpInst(const ICmpInst *cmp,
                                             std::string params[10]) {
    switch (cmp->getPredicate()) {
    case ICmpInst::ICMP_EQ:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "eq";
        break;
    case ICmpInst::ICMP_NE:
        // TODO: Add "not equal" operations to script and change
        // this accordingly
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "eq";
        break;
    case ICmpInst::ICMP_SLT:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "lt";
        break;
    case ICmpInst::ICMP_ULT:
        params[0] = "unsigned";
        params[1] = "comp";
        params[2] = "lt";
        break;
    case ICmpInst::ICMP_SLE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "lte";
        break;
    case ICmpInst::ICMP_ULE:
        params[0] = "unsigned";
        params[1] = "comp";
        params[2] = "lte";
        break;
    case ICmpInst::ICMP_SGT:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "gt";
        break;
    case ICmpInst::ICMP_UGT:
        params[0] = "unsigned";
        params[1] = "comp";
        params[2] = "gt";
        break;
    case ICmpInst::ICMP_SGE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "gte";
        break;
    case ICmpInst::ICMP_UGE:
        params[0] = "unsigned";
        params[1] = "comp";
        params[2] = "gte";
        break;
    default:
        errs() << "Illegal ICmp predicate.\n";
    }
}

void LegupConfig::populateStringsForFCmpInst(const FCmpInst *cmp,
                                             std::string params[10]) {
    switch (cmp->getPredicate()) {
    case FCmpInst::FCMP_OEQ:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "oeq";
        break;
    case FCmpInst::FCMP_UEQ:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "ueq";
        break;
    case FCmpInst::FCMP_ONE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "one";
        break;
    case FCmpInst::FCMP_UNE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "une";
        break;
    case FCmpInst::FCMP_OLT:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "olt";
        break;
    case FCmpInst::FCMP_ULT:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "ult";
        break;
    case FCmpInst::FCMP_OLE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "ole";
        break;
    case FCmpInst::FCMP_ULE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "ule";
        break;
    case FCmpInst::FCMP_OGT:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "ogt";
        break;
    case FCmpInst::FCMP_UGT:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "ugt";
        break;
    case FCmpInst::FCMP_OGE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "oge";
        break;
    case FCmpInst::FCMP_UGE:
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "uge";
        break;
    default:
        errs() << "Illegal FCmp predicate.\n";
    }
}

bool LegupConfig::populateStringsForOneOperandInstr(Instruction *instr,
                                                    std::string params[10]) {
    switch (instr->getOpcode()) {
    case Instruction::FPTrunc:
        params[0] = "altfp";
        params[1] = "truncate";
        break;
    case Instruction::FPExt:
        params[0] = "altfp";
        params[1] = "extend";
        break;
    case Instruction::FPToSI:
        params[0] = "altfp";
        params[1] = "fptosi";
        break;
    case Instruction::SIToFP:
        params[0] = "altfp";
        params[1] = "sitofp";
        break;
    default:
        return false;
    }
    return true;
}

bool LegupConfig::populateStringsForTwoOperandInstr(Instruction *instr,
                                                    std::string params[10]) {
    if (isa<BinaryOperator>(instr)) {
        if (!populateStringsForBinaryOperator(instr, params))
            return false;

    } else if (const ICmpInst *cmp = dyn_cast<ICmpInst>(instr)) {
        populateStringsForICmpInst(cmp, params);
    } else if (const FCmpInst *cmp = dyn_cast<FCmpInst>(instr)) {
        populateStringsForFCmpInst(cmp, params);
    } else {
        // errs() << "Unrecognized instruction: " << *instr << "\n";
        // assert(isa<GetElementPtrInst>(instr) || isa<PHINode>(instr) ||
        //        isa<CallInst>(instr));
    }

    return true;
}

bool LegupConfig::populateStringsForThreeOperandInstr(Instruction *instr,
                                                      std::string params[10]) {
    if (instr->getOpcode() == Instruction::Select) {
        params[0] = "signed";
        params[1] = "comp";
        params[2] = "eq";
        params[3] = "mux";
    } else {
        // DEBUG(errs() << "Unrecognized instruction: " << *instr << "\n");
        return false;
    }
    return true;
}

std::string LegupConfig::assembleOpNameFromStringList(std::string params[10]) {
    std::string op_name = params[0];
    for (int i = 1; params[i] != ""; i++) {
        // errs() << "PARAMS[i] is: " << params[i] << "\n";
        op_name = op_name + "_" + params[i];
    }

    return op_name;
}

std::string LegupConfig::getOpNameFromInst(Instruction *instr) {
    
    // Later take care of signed/unsigned
    std::string params[10];
    int width0 = 0, width1 = 0, width2 = 0;

    switch (instr->getNumOperands()) {
    case 1:
        if (isa<SIToFPInst>(instr)) {
            // altfp_sitofp32 converts int (32) to float (32)
            // altfp_sitofp64 converts int (32) to double (64)
            // width0 should be width of output
            width0 = instr->getType()->getPrimitiveSizeInBits();
        } else {
            width0 = instr->getOperand(0)->getType()->getPrimitiveSizeInBits();
        }
        if (!populateStringsForOneOperandInstr(instr, params))
            return "";
        break;

    case 2:
        width0 = instr->getOperand(0)->getType()->getPrimitiveSizeInBits();
        width1 = instr->getOperand(1)->getType()->getPrimitiveSizeInBits();
        if (!populateStringsForTwoOperandInstr(instr, params))
            return "";
        break;

    case 3:
        width0 = instr->getOperand(0)->getType()->getPrimitiveSizeInBits();
        width1 = instr->getOperand(1)->getType()->getPrimitiveSizeInBits();
        width2 = instr->getOperand(2)->getType()->getPrimitiveSizeInBits();
        if (!populateStringsForThreeOperandInstr(instr, params))
            return "";
        break;
    }

    int BitWidth = maxBitWidth(width0, width1, width2);
    int endindex;
    for (endindex = 0; params[endindex] != ""; endindex++)
        ;

    if (!isSupportedBitwidth(BitWidth) || endindex == 0) {
        // DEBUG(errs() << "Unsupported bitwidth for instruction: " << *instr <<
        // "\n");
        return "";
    }

    params[endindex] = utostr(BitWidth);

    return assembleOpNameFromStringList(params);
}

// checks if the argument is correct. Returns false if incorrect
bool checkArg(const char *argv[], int argNum, const char *option, char *error) {
    assert(argNum > 0);
  if (strcmp(argv[argNum - 1], option) != 0) {
    sprintf(error, "Argument %d is not \"%s\"\n", argNum, option);
    return false;
  }
  return true;
}

bool checkArg2(const char *argv[], int argNum, const char *option,
               const char *option2, char *error) {
  assert(argNum > 0);
  if (strcmp(argv[argNum - 1], option) != 0 &&
      strcmp(argv[argNum - 1], option2) != 0) {
    sprintf(error, "Argument %d is not \"%s\" or \"%s\"\n", argNum, option,
            option2);
    return false;
  }
  return true;
}

/// set_parameter - tcl command to add clock period
int set_parameter(ClientData clientData, Tcl_Interp *interp,
                             int argc, const char *argv[]) {
  static char error[100];
  if (argc != 3) {
    sprintf(error, "%s", "Expecting 3 arguments.");
    interp->result = error;
    return (TCL_ERROR);
  }
  LegupConfig *config = (LegupConfig *)clientData;

  // check arguments are correct
  if (!checkArg(argv, 2, "CLOCK_PERIOD", error)) {
    interp->result = error;
    return (TCL_ERROR);
  }

  config->setClkPeriod(atoi(argv[2]));
  return (TCL_OK);
}


/// set_operation_attributes - tcl command to add hardware operation data
int set_operation_attributes(ClientData clientData, Tcl_Interp *interp,
                             int argc, const char *argv[]) {
  static char error[100];
  if (argc != 21) {
    sprintf(error, "%s", "Expecting 21 arguments.");
    interp->result = error;
    return (TCL_ERROR);
  }
  LegupConfig *config = (LegupConfig *)clientData;

  // check arguments are correct
  if (!checkArg(argv, 2, "-Name", error) ||
      !checkArg(argv, 4, "-Fmax", error) ||
      !checkArg(argv, 6, "-CritDelay", error) ||
      !checkArg(argv, 8, "-StaticPower", error) ||
      !checkArg(argv, 10, "-DynamicPower", error) ||
      !checkArg2(argv, 12, "-LUTs", "-ALUTs", error) ||
      !checkArg(argv, 14, "-Registers", error) ||
      !checkArg2(argv, 16, "-LEs", "-ALMs", error) ||
      !checkArg(argv, 18, "-DSP", error) ||
      !checkArg(argv, 20, "-Latency", error)) {
    interp->result = error;
    return (TCL_ERROR);
  }

  float FMax = atof(argv[4]);
  float CritDelay = atof(argv[6]);
  float StaticPower = atof(argv[8]);
  float DynamicPower = atof(argv[10]);
  int LUTs = atoi(argv[12]);
  int Registers = atoi(argv[14]);
  int LogicElements = atoi(argv[16]);
  int DSPElements = atoi(argv[18]);
  int Latency = atoi(argv[20]);

  config->addOperation(argv[2], FMax, CritDelay, StaticPower, DynamicPower,
                       LUTs, Registers, LogicElements, DSPElements, Latency);
  return (TCL_OK);
}

/// parseTclFile - reads a tcl configuration file and initialize the legupConfig
/// object. Returns false on error.
bool parseTclFile(std::string &ConfigFile, LegupConfig *legupConfig) {
  Tcl_Interp *interp = Tcl_CreateInterp();
  assert(interp);
   
  Tcl_CreateCommand(interp, "set_operation_attributes",
                    set_operation_attributes, legupConfig, 0);

  Tcl_CreateCommand(interp, "set_parameter",
                    set_parameter, legupConfig, 0);


  int result = Tcl_EvalFile(interp, ConfigFile.c_str());

  if (result != TCL_OK) {
    errs() << ConfigFile << ":" << interp->errorLine
           << ": error: " << Tcl_GetStringResult(interp) << "\n";
  }

  Tcl_DeleteInterp(interp);
  // can't call Tcl_Finalize() here - if we have multiple files then we'll
  // get a segfault. But note that without this call Tcl leaks some memory
  // Tcl_Finalize();
  return (result == TCL_OK);
}

}

