#ifndef AES_FUNC_H
#define AES_FUNC_H

void
ByteSub_ShiftRow (int statemt[32], int nb);

int
SubByte (int in);

void
InversShiftRow_ByteSub (int statemt[32], int nb);

int
MixColumn_AddRoundKey (int statemt[32], int nb, int n);

int
AddRoundKey_InversMixColumn (int statemt[32], int nb, int n);

int
AddRoundKey (int statemt[32], int type, int n);

#endif
