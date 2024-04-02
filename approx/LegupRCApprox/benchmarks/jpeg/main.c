/*
+--------------------------------------------------------------------------+
| CHStone : a suite of benchmark programs for C-based High-Level Synthesis |
| ======================================================================== |
|                                                                          |
| * Collected and Modified : Y. Hara, H. Tomiyama, S. Honda,               |
|                            H. Takada and K. Ishii                        |
|                            Nagoya University, Japan                      |
|                                                                          |
| * Remark :                                                               |
|    1. This source code is modified to unify the formats of the benchmark |
|       programs in CHStone.                                               |
|    2. Test vectors are added for CHStone.                                |
|    3. If "main_result" is 0 at the end of the program, the program is    |
|       correctly executed.                                                |
|    4. Please follow the copyright of each benchmark program.             |
+--------------------------------------------------------------------------+
*/
/*
 * Copyright (C) 2008
 * Y. Hara, H. Tomiyama, S. Honda, H. Takada and K. Ishii
 * Nagoya University, Japan
 * All rights reserved.
 *
 * Disclaimer of Warranty
 *
 * These software programs are available to the user without any license fee or
 * royalty on an "as is" basis. The authors disclaims any and all warranties, 
 * whether express, implied, or statuary, including any implied warranties or 
 * merchantability or of fitness for a particular purpose. In no event shall the
 * copyright-holder be liable for any incidental, punitive, or consequential damages
 * of any kind whatsoever arising from the use of these programs. This disclaimer
 * of warranty extends to the user of these programs and user's customers, employees,
 * agents, transferees, successors, and assigns.
 *
 */
#include <stdio.h>

#include "global.h"
#include "decode.h"
#include "init.h"
#include "marker.c"
#include "chenidct.c"
#include "huffman.h"
#include "decode.c"
#include "huffman.c"
#include "jfif_read.c"
#include "jpeg2bmp.c"

void populateInput (unsigned char *inputVector, int *JPEGSIZE, const char *fileName);
void populateOutput (int numElts, int RGBnum, unsigned char outputVector[RGBnum][numElts], const char *fileName);

int
main (int argc, char *argv[])
{
      populateInput(hana_jpg, &JPEGSIZE, argv[1]);
      jpeg2bmp_main ();
      populateOutput(BMP_OUT_SIZE, RGB_NUM, OutData_comp_buf, argv[2]);

      return 0;
}
