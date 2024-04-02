#include <stdlib.h>
#include <stdio.h>

void populateInput (unsigned int bfr[], int inPMV[][2][2][2], int inmvfs[][2][2], int *numVecs, const char *fileName)
{
    FILE* inputFile = fopen(fileName, "r");  
    fscanf (inputFile, "%d\n", numVecs);

    int i, j, k, l;
    for (i = 0; i < *numVecs; i++){
        fscanf (inputFile, "%u, ", &bfr[i]);
	for(j = 0; j < 2; j++)
	    for(k = 0; k < 2; k++)
                for(l = 0; l < 2; l++)         
		    fscanf (inputFile, "%d, ", &inPMV[i][j][k][l]);
	
        for(j = 0; j < 2; j++)
	    for(k = 0; k < 2; k++)
               (j==1 && k==1) ? fscanf (inputFile, "%d\n", &inmvfs[i][j][k]) : fscanf (inputFile, "%d, ", &inmvfs[i][j][k]);
    }
    fclose(inputFile);
       
}

void populateOutput (int outPMV[][2][2][2], int numVecs, const char *fileName)
{   
    FILE* outputFile = fopen(fileName, "w");

    int i, j, k;
    for (i = 0; i < numVecs; i++){
        for(j = 0; j < 2; j++)
	     for(k = 0; k < 2; k++)         
		  fprintf (outputFile, "%i\n", outPMV[i][j][0][k]);
	
    }
    fclose(outputFile);
}

