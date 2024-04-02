# application 
export NAME = sobel

# bench I/O library directory
export BENCH_IOLIB_DIR = IOLib/

# training vectors directory
export TRAINING_VECS_DIR = inputs/training/

# test vectors directory
export TEST_VECS_DIR = inputs/test/

# timing constraint to execute bytecodes 
export TIMEOUT = 10

# actual bitwidth of output values (PSNR calculation)
export OUTPUT_BITWIDTH = 8

# max number of approx designs to explore at each iteration (threaded)
export MAX_BRANCHES = 8

# print information to stdout
export VERBOSE = 0

# LUTs constraint (exact: 1212) 
MAX_LUTS = 1090 

# REGs constraint (exact: 1222) 
MAX_REGS = 1099 

# DSPs constraint (exact: 0)
MAX_DSPS = 0  

# legup configuration (overleaps the default configuration)
LOCAL_CONFIG = -legup-config=config.tcl

# loop unrolling
UNROLL := -unroll-allow-partial -unroll-count=10 -unroll-threshold=1000 -unroll-runtime -debug

include ../Makefile.common
LEVEL = ../../..
include $(LEVEL)/Makefile.common
