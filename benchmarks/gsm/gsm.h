#ifndef GSM_H
#define GSM_H

#include "gsm_private.h"

#define N 160
#define M 8

/* top-level function */
/* s: 0..159 signals IN/OUT */
/* LARc: 0..7 LARc's OUT    */
void Gsm_LPC_Analysis(word indata[N], word LARc[M]);

#endif // GSM_H