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
/* aes.h */
/*
 * Copyright (C) 2005
 * Akira Iwata & Masayuki Sato
 * Akira Iwata Laboratory,
 * Nagoya Institute of Technology in Japan.
 *
 * All rights reserved.
 *
 * This software is written by Masayuki Sato.
 * And if you want to contact us, send an email to Kimitake Wakayama
 * (wakayama@elcom.nitech.ac.jp)
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. All advertising materials mentioning features or use of this software must
 *    display the following acknowledgment:
 *    "This product includes software developed by Akira Iwata Laboratory,
 *    Nagoya Institute of Technology in Japan (http://mars.elcom.nitech.ac.jp/)."
 *
 * 4. Redistributions of any form whatsoever must retain the following
 *    acknowledgment:
 *    "This product includes software developed by Akira Iwata Laboratory,
 *     Nagoya Institute of Technology in Japan (http://mars.elcom.nitech.ac.jp/)."
 *
 *   THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY.
 *   AKIRA IWATA LABORATORY DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
 *   SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS,
 *   IN NO EVENT SHALL AKIRA IWATA LABORATORY BE LIABLE FOR ANY SPECIAL,
 *   INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
 *   FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 *   NEGLIGENCE OR OTHER TORTUOUS ACTION, ARISING OUT OF OR IN CONNECTION
 *   WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */

#ifndef AES_H
#define AES_H

/* constants for input/output sizes */
#define IN_SIZE 32
#define OUT_SIZE 16

#define AES_POLY 0x11B // AES irreducible polynomial (283 in decimal)

// Define constants for AES
#define AES_BLOCK_SIZE 4 // Number of words in a block
#define MAX_WORDS 60     // Maximum number of words for expanded keys (256-bit AES with 14 rounds)

/* key generate */
int KeySchedule (int type, int key[32]);
/* ********* ByteSub & ShiftRow ********* */
void ByteSub_ShiftRow (int statemt[32], int nb);
/* ********* InversShiftRow & ByteSub ********* */
void InversShiftRow_ByteSub (int statemt[32], int nb);
/* ******** MixColumn ********** */
int MixColumn_AddRoundKey (int statemt[32], int nb, int n);
/* ******** InversMixColumn ********** */
int AddRoundKey_InversMixColumn (int statemt[32], int nb, int n);
/* ******** AddRoundKey ********** */
int AddRoundKey (int statemt[32], int type, int n);

/* encrypt/decrypt functions */
int encrypt(int statemt[IN_SIZE], int key[IN_SIZE], int type);
int decrypt(int statemt[IN_SIZE], int key[IN_SIZE], int type);

/* top-level function */
int aes_main (int statemt[IN_SIZE], int key[IN_SIZE]);

#endif // AES_H
