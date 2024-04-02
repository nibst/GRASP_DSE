# application 
export NAME=mpeg2

# bench I/O library directory
export BENCH_IOLIB_DIR = IOLib/

# training vectors directory
export TRAINING_VECS_DIR = inputs/training/

# test vectors directory
export TEST_VECS_DIR = inputs/test/

# timing constraint when executing bytecodes
export TIMEOUT = 10

# max bitwidth of output values (for PSNR calculation)
export OUTPUT_BITWIDTH = 5

# max number of approx designs to explore at each iteration (threaded)
export MAX_BRANCHES = 8

# print information to stdout
export VERBOSE = 0

# LUTs constraint (exact: 9883)
MAX_LUTS = 8894 

# REGs constraint (exact: 8150)
MAX_REGS = 7335

# DSPs constraint (exact: 0)
MAX_DSPS = 0

# legup configuration (overleaps the default configuration)
LOCAL_CONFIG = -legup-config=config.tcl

include ../Makefile.common
LEVEL = ../../..
include $(LEVEL)/Makefile.common
