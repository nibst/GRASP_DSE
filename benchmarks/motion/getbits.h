#ifndef GETBITS_H
#define GETBITS_H

#define Num 2048

extern const unsigned char inRdbfr[Num];

int read (unsigned char *s1, const unsigned char *s2, int n);
void Fill_Buffer();
unsigned int Show_Bits(int n);
unsigned int Get_Bits1();
void Flush_Buffer(int n);
unsigned int Get_Bits(int n);
//int Get_Byte();  nao ha essa funcao no .c

#endif
