#include <stdlib.h>
#include <stdio.h>

void populateInput (int *inputVector, int numElts, const char *fileName)
{
    FILE* inputFile = fopen(fileName, "r");  

    int i;
    for (i = 0; i < numElts; i++){
        fscanf (inputFile, "%i", &inputVector[i]);
    }
    fprintf(stderr,"input good");
   
    fclose(inputFile);
       
}

void populateOutput (int *outputVector, int numElts, const char *fileName)
{   
    FILE* outputFile = fopen(fileName, "w");

    int i;
    for (i = 0; i < numElts; i++)
        fprintf (outputFile, "%i\n", outputVector[i]); 
     
    fclose(outputFile);
}

