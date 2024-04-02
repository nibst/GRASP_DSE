#include <stdio.h>
#include <stdlib.h>

#define ROWS 512
#define COLS 512
#define DATASIZE ROWS*COLS

//__attribute__ ((noinline)) 
void __attribute__ ((always_inline)) sobel(int inrows,  int incols,  unsigned char * indata, 
		unsigned char * outdata, int * GX, int * GY)
{
   unsigned int		X, Y;
   /*---------------------------------------------------
		SOBEL ALGORITHM STARTS HERE
   ---------------------------------------------------*/
   for(Y=1; Y<inrows-1; Y++)  {
	for(X=1; X<incols-1; X++)  {
         long sumX = 0;
         long sumY = 0;
         int  SUM = 0;
         int t1,t2,c1,c2,c3;

         /* image boundaries */
         t1 = Y==0; t2 = Y==inrows-1;
         c1 = t1 || t2;
         c1 = !c1;

         t1 = X==0; t2 = X==inrows-1;
         c2 = t1 || t2;
         c2 = !c2;

         c3 = c1 && c2;

	     if(c3)
	     /* Convolution starts here */
	     {
           int			I, J;

	       /*-------X GRADIENT APPROXIMATION------*/
	       for(I=-1; I<=1; I++)  {
		   for(J=-1; J<=1; J++)  {
		      sumX = sumX + (int)( indata[X + I + (Y + J)*incols] * GX[3*I + J + 4]);
		      sumY = sumY + (int)( indata[X + I + (Y + J)*incols] * GY[3*I + J + 4]);
		   }
	       }
	       if(sumX>255)  sumX=255;
	       if(sumX<0)    sumX=0;

	       /*-------Y GRADIENT APPROXIMATION-------*/
	       if(sumY>255)   sumY=255;
	       if(sumY<0)     sumY=0;

	       SUM = sumX + sumY; /*---GRADIENT MAGNITUDE APPROXIMATION (Myler p.218)----*/
             }
//         printf("y=%d ; x=%d --> SUM = %d", Y,X,SUM);
	     outdata[X + Y*incols] = 255 - (unsigned char)(SUM);  /* make edges black and background white */
//         printf(" --> outdata[%d] = %d\n", X + Y*incols, outdata[X + Y*incols]);
	}
   }
}

unsigned char indata[DATASIZE];
unsigned char outdata[DATASIZE];

void populateInput (unsigned char *inputVector, int numElts, const char *fileName);
void populateOutput (unsigned char *outputVector, int numElts, const char *fileName);

int main(int argc, char *argv[])
{
  int GX[9];
  int GY[9];
  
  /* 3x3 GX Sobel mask.  Ref: www.cee.hw.ac.uk/hipr/html/sobel.html */
   GX[0*3+0] = -1; GX[0*3+1] = 0; GX[0*3+2] = 1;
   GX[1*3+0] = -2; GX[1*3+1] = 0; GX[1*3+2] = 2;
   GX[2*3+0] = -1; GX[2*3+1] = 0; GX[2*3+2] = 1;

  /* 3x3 GY Sobel mask.  Ref: www.cee.hw.ac.uk/hipr/html/sobel.html */
   GY[0*3+0] =  1; GY[0*3+1] =  2; GY[0*3+2] =  1;
   GY[1*3+0] =  0; GY[1*3+1] =  0; GY[1*3+2] =  0;
   GY[2*3+0] = -1; GY[2*3+1] = -2; GY[2*3+2] = -1;

   populateInput(indata, DATASIZE, argv[1]);
   sobel(ROWS, COLS, indata, outdata, (int*)GX, (int*)GY);
   populateOutput(outdata, DATASIZE, argv[2]);

  return 0;
}

