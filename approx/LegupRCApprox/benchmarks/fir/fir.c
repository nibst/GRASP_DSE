,/*
    FIR with 8000 inputs, 16-bit, 25 taps
    
*/

#include <stdio.h>

#define INPUTSIZE 8000
#define TAPS 25

int inputs[INPUTSIZE];
int outputs[INPUTSIZE];
//__attribute__ ((noinline))
int __attribute__((always_inline)) FIRFilterStreaming (int in, int coefficients[], int previous[]){
    int j, temp;
    for(j=(TAPS-1); j>=1; j-=1 ){

         previous[j] = previous[j-1];

    }
    previous[0] = in;

    if (previous[TAPS-1] == 0)
        return 0;
    else {
        temp = 0;

        for (j = 0; j < TAPS; j++){
            temp += previous[TAPS - j - 1]*coefficients[j];
        }
        return temp;
    }

}

void populateInput (int *inputVector, int numElts, const char *fileName);
void populateOutput (int *outputVector, int numElts, const char *fileName);

int main(int argc, char *argv[]){

    int previous[TAPS] = {0};
    int coefficients[TAPS] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25};
    int i;
    populateInput(inputs, INPUTSIZE, argv[1]);
    for (i = 0; i < INPUTSIZE; i++){
        outputs[i] = FIRFilterStreaming (inputs[i], coefficients, previous);
    
    }
    populateOutput(outputs, INPUTSIZE, argv[2]);

    return 0;
}
