# application 
export NAME=main

# bench I/O library directory
export BENCH_IOLIB_DIR = IOLib/

# training vectors directory
export TRAINING_VECS_DIR = inputs/training/

# test vectors directory
export TEST_VECS_DIR = inputs/test/

# timing constraint when executing bytecodes
export TIMEOUT = 10

# actual bitwidth of output values (PSNR calculation)
export OUTPUT_BITWIDTH = 8

# max number of approx designs to explore at each iteration (threaded)
export MAX_BRANCHES = 8

# print information to stdout
export VERBOSE = 0

# LUTs constraint (exact: 27431)
MAX_LUTS = 24687

# REGs constraint (exact: 17896)
MAX_REGS = 16106

# DSPs constraint (exact: 104)
MAX_DSPS = 93

# legup configuration (overleaps the default configuration)
LOCAL_CONFIG = -legup-config=config.tcl

include ../Makefile.common
LEVEL = ../../..
include $(LEVEL)/Makefile.common
