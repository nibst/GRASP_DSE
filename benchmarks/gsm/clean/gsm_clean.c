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
#include <stdio.h>
#include "add.c"


#ifndef	PRIVATE_H
#define	PRIVATE_H

typedef short word;		/* 16 bit signed int    */
typedef long longword;		/* 32 bit signed int    */

#define	MIN_WORD	((-32767)-1)
#define	MAX_WORD	( 32767)

#define	SASR(x, by)	((x) >> (by))

#define GSM_MULT_R(a, b)	gsm_mult_r(a, b)
#define GSM_MULT(a, b)		gsm_mult(a, b)
#define GSM_ADD(a, b)		gsm_add(a, b)
#define GSM_ABS(a)		gsm_abs(a)

#endif /* PRIVATE_H */

/*
+--------------------------------------------------------------------------+
| * Test Vectors (added for CHStone)                                       |
|     inData : input data                                                  |
|     outData, outLARc : expected output data                              |
+--------------------------------------------------------------------------+
*/
#define N 160
#define M 8
const word inData[N] =
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

const word outData[N] =
  { 80, 10848, 1888, -10288, 7616, 29712, 20480, -29216, -18944, -29808,
  -32016, 1600, 15744, -3088, -17408, -22128, 6800, -13280, 3824, -16272,
    -1568, -12528, -27104,
  -192, -25584, 4704, -30432, 15264, -1392, 11424, 11376, 4992, 7872, -1904,
    9120, -31728, -25232,
  -14160, 17984, 32432, -12432, -15936, -21616, 7904, 1696, 28112, 3616,
    22128, -5568, -20112,
  12384, 9184, -24544, 12480, 21552, -17840, -13648, 20272, 9984, 17648,
    -11456, -17328, -10544,
  -27104, 208, 27616, 2512, 7168, -29728, -22448, 30032, -2368, 12816, 304,
    -25552, 9088, 29024,
  -6560, -20304, -14352, -7552, -21712, -3680, -30080, -3184, -30976, 8576,
    27120, 3408, -4608,
  -22304, -17136, 13792, -1088, -14624, 22064, -13552, 32640, 16688, -8480,
    -12736, 10496, 20752,
  6704, -26848, -31008, 3792, -19856, -20432, -30304, 32416, -13232, 9008,
    18256, 2400, -8000,
  -14832, -5856, 7120, 29824, -31888, 17952, 28832, -31296, 31824, -27504,
    12272, -5584, -22112,
  9200, -22544, 15680, -12272, 7216, -23744, -12848, -5856, 7520, 17344,
    13776, -3088, -17808,
  -9648, 26672, 7904, 2480, 3184, 29408, -20224, -2768, 24080, -7968, -10432,
    -11936, -14832,
  -6656, 32064, 4016, 10464, 15152
};

const word outLARc[M] = { 32, 33, 22, 13, 7, 5, 3, 2 };

void
Gsm_LPC_Analysis (word * s /* 0..159 signals       IN/OUT  */ ,
		  word * LARc /* 0..7   LARc's        OUT     */ )
{
  longword L_ACF[9];
//Autocorrelation (so, L_ACF);
//Autocorrelation (word * s /* [0..159]     IN/OUT  */ ,longword * L_ACF /* [0..8]       OUT     */ )
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
  for (k = 0; k <= 159; k++)
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
//Reflection_coefficients (L_ACF, LARc);
//Reflection_coefficients (longword * L_ACF /* 0...8        IN      */ ,register word * r /* 0...7        OUT     */ )
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
      for (i = 8; i > 0; i--)
        *LARc++ = 0;
        return;
    }

  temp = gsm_norm (L_ACF[0]);
  for (i = 0; i <= 8; i++)
    ACF[i] = SASR (L_ACF[i] << temp, 16);

  /*   Initialize array P[..] and K[..] for the recursion.
   */

  for (i = 1; i <= 7; i++)
    K[i] = ACF[i];
  for (i = 0; i <= 8; i++)
    P[i] = ACF[i];

  /*   Compute reflection coefficients
   */
  for (n = 1; n <= 8; n++, LARc++)
  {
  //#pragma HLS LOOP_TRIPCOUNT min=1 max=8

    temp = P[1];
    temp = GSM_ABS (temp);
    if (P[0] < temp)
    {
      for (i = n; i <= 8; i++)
      //#pragma HLS LOOP_TRIPCOUNT min=1 max=8
        *LARc++ = 0;
      return;
    }

    *LARc = gsm_div (temp, P[0]);

    if (P[1] > 0)
      *LARc = -*LARc;		/* r[n] = sub(0, r[n]) */
    if (n == 8)
      return;

    /*  Schur recursion
      */
    temp = GSM_MULT_R (P[1], *LARc);
    P[0] = GSM_ADD (P[0], temp);

    for (m = 1; m <= 8 - n; m++)
    {
      //#pragma HLS LOOP_TRIPCOUNT min=1 max=7
      temp = GSM_MULT_R (K[m], *LARc);
      P[m] = GSM_ADD (P[m + 1], temp);

      temp = GSM_MULT_R (P[m + 1], *LARc);
      K[m] = GSM_ADD (K[m], temp);
    }
  }
}
//Transformation_to_Log_Area_Ratios (LARc);
//Transformation_to_Log_Area_Ratios (register word * r /* 0..7    IN/OUT */ )
{
  register word temp;
  register int i;
  /* Computation of the LAR[0..7] from the r[0..7]
   */
  for (i = 1; i <= 8; i++, LARc++)
    {

      temp = *LARc;
      temp = temp < 0 ? (temp == MIN_WORD ? MAX_WORD : -temp) : temp;

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

      *LARc = *LARc < 0 ? -temp : temp;
    }
}

//Quantization_and_coding (LARc);

//Quantization_and_coding (register word * LAR /* [0..7]       IN/OUT  */ )
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
		temp = GSM_MULT( A,   *LARc );	\
		temp = GSM_ADD(  temp,   B );	\
		temp = GSM_ADD(  temp, 256 );	\
		temp = SASR(     temp,   9 );	\
		*LARc  =  temp>MAC ? MAC - MIC : (temp<MIC ? 0 : temp - MIC); \
		LARc++;

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
}

int
main ()
{
  int i;
  int main_result;
  word so[N];
  word LARc[M];
      main_result = 0;

  for (i = 0; i < N; i++)
    so[i] = inData[i];

  Gsm_LPC_Analysis (so, LARc);

  for (i = 0; i < N; i++)
    main_result += (so[i] != outData[i]);
  for (i = 0; i < M; i++)
	  main_result += (LARc[i] != outLARc[i]);

  printf ("%d\n", main_result);
  return main_result;
}