#include <stdio.h>
#include <stdlib.h>
#define SIZE 8000

void example(int a[SIZE], int b[SIZE]) {

  int buff[SIZE];
  example_label0:for (int i = 0; i < SIZE; ++i) {
    buff[i] = a[i];
    buff[i] = buff[i] + 100;
    b[i] = buff[i];
  }
}
extern "C" void populateInput (int *inputVector, int numElts, const char *fileName);
extern "C" void populateOutput (int *outputVector, int numElts, const char *fileName);
int main (int argc, char *argv[])
{ 
  int indata[SIZE];
  int outdata[SIZE];

  populateInput(indata, SIZE, argv[1]);
  example(indata,outdata);
  populateOutput(outdata, SIZE, argv[2]);
    
  return 0; 
}