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

#define Num 2048
#define MAX_VECS 380

/*
+--------------------------------------------------------------------------+
| * Test Vectors (added for CHStone)                                       |
|     inRdbfr, inPMV, inPMV : input data                                   |
|     outPMV, outmvfs : expected output data                               |
+--------------------------------------------------------------------------+
*/
const unsigned char inRdbfr[Num]={153};
const unsigned char out_ld_Rdptr[Num];

int inPMV[MAX_VECS][2][2][2];
int inmvfs[MAX_VECS][2][2];
unsigned int bfr[MAX_VECS]={689523667};

int numVecs;
int evalue;
#include "config.h"
#include "global.h"
#include "getbits.c"
#include "getvlc.h"
#include "getvlc.c"
#include "motion.c"

void
Initialize_Buffer ()
{
  ld_Incnt = 0;
  ld_Rdptr = ld_Rdbfr + 2048;
  ld_Rdmax = ld_Rdptr;
  ld_Bfr = 0;
  Flush_Buffer (0);		/* fills valid data into bfr */
}

void populateInput (unsigned int bfr[], int inPMV[][2][2][2], int inmvfs[][2][2], int *numVecs, const char *fileName);
void populateOutput (int outPMV[][2][2][2], int numVecs, const char *fileName);

int
main (int argc, char *argv[])
{
  int dmvector[2] = {24960, 0};
  int s, motion_vector_count, mv_format, h_r_size, v_r_size, dmv, mvscale;
  int i;
  evalue = 0;
  System_Stream_Flag = 0;
  s = 0;
  motion_vector_count = 1;
  mv_format = 1;
  h_r_size = 1;
  v_r_size = 1;
  dmv = 0;
  mvscale = 0;
      
  Initialize_Buffer ();
  populateInput(bfr, inPMV, inmvfs, &numVecs, argv[1]);
	
  for(i = 0; i < numVecs; i++){
      ld_Bfr = bfr[i];
      motion_vectors (inPMV[i], dmvector, inmvfs[i], s,
		      motion_vector_count, mv_format, h_r_size, v_r_size, dmv,
		      mvscale);
  }
  
  populateOutput(inPMV, numVecs, argv[2]);
    
  return 0;

}
