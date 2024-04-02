#include <stdlib.h>
#include <stdio.h>

void populateInput (unsigned char *inputVector, int *JPEGSIZE, const char *fileName)
{
    FILE* inputFile = fopen(fileName, "r");    
    fscanf (inputFile, "%i", &(*JPEGSIZE)); 
    int i;
    for (i = 0; i < *JPEGSIZE; i++)
        fscanf (inputFile, "%hhu", &inputVector[i]);
    fclose(inputFile);
}


void populateOutput (int numElts, int RGBnum, unsigned char outputVector[RGBnum][numElts], const char *fileName)
{   
    FILE* outputFile = fopen(fileName, "w");
    int i, j;
    for (i = 0; i < RGBnum; i++){
		for (j = 0; j < numElts; j++){
        	fprintf (outputFile, "%hhu\n", outputVector[i][j]); 
        }
    }     
    fclose(outputFile);
}


