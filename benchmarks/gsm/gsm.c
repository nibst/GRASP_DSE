#include "gsm.h"
#include "gsm_lpc.h"

/* top-level function */
/* s: 0..159 signals IN/OUT */
/* LARc: 0..7 LARc's OUT    */
void Gsm_LPC_Analysis(word indata[N], word LARc[M])
{
    longword L_ACF[9];

    Autocorrelation(indata, L_ACF);
    Reflection_coefficients(L_ACF, LARc);
    Transformation_to_Log_Area_Ratios(LARc);
    Quantization_and_coding(LARc);
}
