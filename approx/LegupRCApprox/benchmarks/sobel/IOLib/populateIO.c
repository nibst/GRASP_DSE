#include <stdlib.h>
#include <stdio.h>

void populateInput (unsigned char *inputVector, int numElts, const char *fileName)
{
    FILE* inputFile = fopen(fileName, "r");    
    
    int i;
    for (i = 0; i < numElts; i++)
        fscanf (inputFile, "%hhu", &inputVector[i]);
    
    fclose(inputFile);
       
}

void populateOutput (unsigned char *outputVector, int numElts, const char *fileName)
{   
    FILE* outputFile = fopen(fileName, "w");
    
    int i;    
    for (i = 0; i < numElts; i++)
        fprintf (outputFile, "%hhu\n", outputVector[i]); 
            
    fclose(outputFile);
}


