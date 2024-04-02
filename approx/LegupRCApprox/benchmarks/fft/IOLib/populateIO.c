#include <stdlib.h>
#include <stdio.h>

void populateInput (short *inputReal, int numElts, const char *fileName)
{
    FILE* inputFile = fopen(fileName, "r");    
    for (int i = 0; i < numElts; i++){
	if (i < 8000)
        	fscanf (inputFile, "%hi", &inputReal[i]);
	else
		inputReal[i] = 0;
    }
    fclose(inputFile);
       
}

void populateOutput (short *outputReal, short *outputImag, int numElts, const char *fileName)
{   
    FILE* outputFile = fopen(fileName, "w");
        
    for (int i = 0; i < numElts; i++)
        fprintf (outputFile, "%hi\n%hi\n", outputReal[i], outputImag[i]); 
             
    fclose(outputFile);
}

