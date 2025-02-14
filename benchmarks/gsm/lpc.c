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
 * Copyright 1992 by Jutta Degener and Carsten Bormann, Technische
 * Universitaet Berlin.  See the accompanying file "COPYRIGHT" for
 * details.  THERE IS ABSOLUTELY NO WARRANTY FOR THIS SOFTWARE.
 */

/* $Header: /home/kbs/jutta/src/gsm/gsm-1.0/src/RCS/lpc.c,v 1.5 1994/12/30 23:14:54 jutta Exp $ */

#include "private.h"
#include "add.h"
#include "lpc.h"


/*
 *  4.2.4 .. 4.2.7 LPC ANALYSIS SECTION
 */

/* 4.2.4 */


void
Autocorrelation (word * s /* [0..159]     IN/OUT  */ ,
		 longword * L_ACF /* [0..8]       OUT     */ )
/*
 *  The goal is to compute the array L_ACF[k].  The signal s[i] must
 *  be scaled in order to avoid an overflow situation.
 */
{
  register int k, i;

  word temp;
  word smax;
  word scalauto, n;
  word *sp;
  word sl;

  /*  Search for the maximum.
   */
  smax = 0;
Autocorrelation_label0: for (k = 0; k <= 159; k++)
    {
      temp = GSM_ABS (s[k]);
      if (temp > smax)
	      smax = temp;
    }

    /*  Computation of the scaling factor.
    */
    if (smax == 0)
      scalauto = 0;
    else
      scalauto = 4 - gsm_norm ((longword) smax << 16);	/* sub(4,..) */

    if (scalauto > 0 && scalauto <= 4)
      {
        n = scalauto;
        for (k = 0; k <= 159; k++)
           s[k] = GSM_MULT_R (s[k], 16384 >> (n - 1));
      }

  /*  Compute the L_ACF[..].
   */
  {
    sp = s;
    sl = *sp;

#define STEP(k)	 L_ACF[k] += ((longword)sl * sp[ -(k) ]);

#define NEXTI	 sl = *++sp
    for (k = 8; k >= 0; k--)
      L_ACF[k] = 0;

    STEP (0);
    NEXTI;
    STEP (0);
    STEP (1);
    NEXTI;
    STEP (0);
    STEP (1);
    STEP (2);
    NEXTI;
    STEP (0);
    STEP (1);
    STEP (2);
    STEP (3);
    NEXTI;
    STEP (0);
    STEP (1);
    STEP (2);
    STEP (3);
    STEP (4);
    NEXTI;
    STEP (0);
    STEP (1);
    STEP (2);
    STEP (3);
    STEP (4);
    STEP (5);
    NEXTI;
    STEP (0);
    STEP (1);
    STEP (2);
    STEP (3);
    STEP (4);
    STEP (5);
    STEP (6);
    NEXTI;
    STEP (0);
    STEP (1);
    STEP (2);
    STEP (3);
    STEP (4);
    STEP (5);
    STEP (6);
    STEP (7);

    for (i = 8; i <= 159; i++)
      {

	NEXTI;

	STEP (0);
	STEP (1);
	STEP (2);
	STEP (3);
	STEP (4);
	STEP (5);
	STEP (6);
	STEP (7);
	STEP (8);
      }

    for (k = 8; k >= 0; k--)
      L_ACF[k] <<= 1;

  }
  /*   Rescaling of the array s[0..159]
   */
  if (scalauto > 0)
    for (k = 159; k >= 0; k--)
      *s++ <<= scalauto;
}

/* 4.2.5 */

void
Reflection_coefficients (longword * L_ACF /* 0...8        IN      */ ,
			 register word * r /* 0...7        OUT     */ )
{
  register int i, m, n;
  register word temp;
  word ACF[9];			/* 0..8 */
  word P[9];			/* 0..8 */
  word K[9];			/* 2..8 */

  /*  Schur recursion with 16 bits arithmetic.
   */

  if (L_ACF[0] == 0)
    {
      Reflection_coefficients_label0:for (i = 8; i > 0; i--)
	      *r++ = 0;
      return;
    }

  temp = gsm_norm (L_ACF[0]);
  Reflection_coefficients_label1:for (i = 0; i <= 8; i++)
    ACF[i] = SASR (L_ACF[i] << temp, 16);

  /*   Initialize array P[..] and K[..] for the recursion.
   */

  Reflection_coefficients_label2:for (i = 1; i <= 7; i++)
    K[i] = ACF[i];
  Reflection_coefficients_label3:for (i = 0; i <= 8; i++)
    P[i] = ACF[i];

  /*   Compute reflection coefficients
   */
  Reflection_coefficients_label4:for (n = 1; n <= 8; n++, r++)
    {
    #pragma HLS LOOP_TRIPCOUNT min=1 max=8

      temp = P[1];
      temp = GSM_ABS (temp);
      if (P[0] < temp)
        {
          Reflection_coefficients_label6:for (i = n; i <= 8; i++)
          #pragma HLS LOOP_TRIPCOUNT min=1 max=8
            *r++ = 0;
          return;
        }

      *r = gsm_div (temp, P[0]);

      if (P[1] > 0)
	    *r = -*r;		/* r[n] = sub(0, r[n]) */
      if (n == 8)
	    return;

      /*  Schur recursion
       */
      temp = GSM_MULT_R (P[1], *r);
      P[0] = GSM_ADD (P[0], temp);

      Reflection_coefficients_label5:for (m = 1; m <= 8 - n; m++)
        {
          #pragma HLS LOOP_TRIPCOUNT min=1 max=7
          temp = GSM_MULT_R (K[m], *r);
          P[m] = GSM_ADD (P[m + 1], temp);

          temp = GSM_MULT_R (P[m + 1], *r);
          K[m] = GSM_ADD (K[m], temp);
        }
;    }
}

/* 4.2.6 */

void
Transformation_to_Log_Area_Ratios (register word * r /* 0..7    IN/OUT */ )
/*
 *  The following scaling for r[..] and LAR[..] has been used:
 *
 *  r[..]   = integer( real_r[..]*32768. ); -1 <= real_r < 1.
 *  LAR[..] = integer( real_LAR[..] * 16384 );
 *  with -1.625 <= real_LAR <= 1.625
 */
{
  register word temp;
  register int i;


  /* Computation of the LAR[0..7] from the r[0..7]
   */
  for (i = 1; i <= 8; i++, r++)
    {

      temp = *r;
      temp = GSM_ABS (temp);

      if (temp < 22118)
	{
	  temp >>= 1;
	}
      else if (temp < 31130)
	{
	  temp -= 11059;
	}
      else
	{
	  temp -= 26112;
	  temp <<= 2;
	}

      *r = *r < 0 ? -temp : temp;
    }
}

/* 4.2.7 */

void
Quantization_and_coding (register word * LAR /* [0..7]       IN/OUT  */ )
{
  register word temp;


  /*  This procedure needs four tables; the following equations
   *  give the optimum scaling for the constants:
   *  
   *  A[0..7] = integer( real_A[0..7] * 1024 )
   *  B[0..7] = integer( real_B[0..7] *  512 )
   *  MAC[0..7] = maximum of the LARc[0..7]
   *  MIC[0..7] = minimum of the LARc[0..7]
   */

#	undef STEP
#	define	STEP( A, B, MAC, MIC )		\
		temp = GSM_MULT( A,   *LAR );	\
		temp = GSM_ADD(  temp,   B );	\
		temp = GSM_ADD(  temp, 256 );	\
		temp = SASR(     temp,   9 );	\
		*LAR  =  temp>MAC ? MAC - MIC : (temp<MIC ? 0 : temp - MIC); \
		LAR++;

  STEP (20480, 0, 31, -32);
  STEP (20480, 0, 31, -32);
  STEP (20480, 2048, 15, -16);
  STEP (20480, -2560, 15, -16);

  STEP (13964, 94, 7, -8);
  STEP (15360, -1792, 7, -8);
  STEP (8534, -341, 3, -4);
  STEP (9036, -1144, 3, -4);

#	undef	STEP
}
#define N 160
#define M 8



void
Gsm_LPC_Analysis ()
{
  word inData[N] =
  { 81, 10854, 1893, -10291, 7614, 29718, 20475, -29215, -18949, -29806,
  -32017, 1596, 15744, -3088, -17413, -22123, 6798, -13276, 3819, -16273,
    -1573, -12523, -27103,
  -193, -25588, 4698, -30436, 15264, -1393, 11418, 11370, 4986, 7869, -1903,
    9123, -31726,
  -25237, -14155, 17982, 32427, -12439, -15931, -21622, 7896, 1689, 28113,
    3615, 22131, -5572,
  -20110, 12387, 9177, -24544, 12480, 21546, -17842, -13645, 20277, 9987,
    17652, -11464, -17326,
  -10552, -27100, 207, 27612, 2517, 7167, -29734, -22441, 30039, -2368, 12813,
    300, -25555, 9087,
  29022, -6559, -20311, -14347, -7555, -21709, -3676, -30082, -3190, -30979,
    8580, 27126, 3414,
  -4603, -22303, -17143, 13788, -1096, -14617, 22071, -13552, 32646, 16689,
    -8473, -12733, 10503,
  20745, 6696, -26842, -31015, 3792, -19864, -20431, -30307, 32421, -13237,
    9006, 18249, 2403,
  -7996, -14827, -5860, 7122, 29817, -31894, 17955, 28836, -31297, 31821,
    -27502, 12276, -5587,
  -22105, 9192, -22549, 15675, -12265, 7212, -23749, -12856, -5857, 7521,
    17349, 13773, -3091,
  -17812, -9655, 26667, 7902, 2487, 3177, 29412, -20224, -2776, 24084, -7963,
    -10438, -11938,
  -14833, -6658, 32058, 4020, 10461, 15159
};
  word LARc[M];
  longword L_ACF[9];

  Autocorrelation (inData, L_ACF);
  Reflection_coefficients (L_ACF, LARc);
  Transformation_to_Log_Area_Ratios (LARc);
  Quantization_and_coding (LARc);
}
