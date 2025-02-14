#ifndef GSM_LPC_H
#define GSM_LPC_H

#include "gsm_private.h"
#include "gsm_add.h"

#define GSM_MULT_R(a, b)    gsm_mult_r(a, b)
#define GSM_MULT(a, b)		gsm_mult(a, b)
#define GSM_ADD(a, b)		gsm_add(a, b)
#define GSM_ABS(a)		    gsm_abs(a)

/* 4.2.4 */
/* s: [0..159] IN/OUT */
/* L_ACF: [0..8] OUT */
void Autocorrelation(word *s, longword *L_ACF);

/* 4.2.5 */
/* L_ACF [0...8] IN */
/* r: [0..7] OUT    */
void Reflection_coefficients(longword *L_ACF, register word *r);

/* 4.2.6 */
/* r: [0..7] IN/OUT */
void Transformation_to_Log_Area_Ratios(register word *r);

/* 4.2.7 */
/* LAR: [0..7] IN/OUT */
void Quantization_and_coding(register word *LAR);

#endif // GSM_LPC_H