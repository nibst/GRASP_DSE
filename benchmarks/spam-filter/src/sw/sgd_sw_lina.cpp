/*===============================================================*/
/*                                                               */
/*                         sgd_sw.cpp                            */
/*                                                               */
/*              Software version for spam filtering.             */
/*                                                               */
/*===============================================================*/

#define SW

#include "sgd_sw.h"
#include "math.h"

// top-level function
void SgdLR_sw(DataType data[NUM_FEATURES * NUM_TRAINING],
              LabelType label[NUM_TRAINING], FeatureType theta[NUM_FEATURES]) {
  // intermediate variable for storing gradient
  FeatureType gradient[NUM_FEATURES];

  // main loop
  // runs for multiple epochs
  for (int epoch = 0; epoch < NUM_EPOCHS; epoch++) {
    // in each epoch, go through each training instance in sequence
    for (int training_id = 0; training_id < NUM_TRAINING; training_id++) {
      // dot product between parameter vector and data sample
      FeatureType dot = 0;
      for (int i = 0; i < NUM_FEATURES; i++)
        dot += theta[i] * data[NUM_FEATURES * training_id + i];

      // sigmoid
      FeatureType prob = 1.0f / (1.0f + expf(-dot));

      // compute gradient
      for (int i = 0; i < NUM_FEATURES; i++)
        gradient[i] =
            (prob - label[training_id]) * data[NUM_FEATURES * training_id + i];

      // update parameter vector
      for (int i = 0; i < NUM_FEATURES; i++)
        theta[i] += (-STEP_SIZE) * gradient[i];
    }
  }
}

int main(){
  DataType *data = (DataType *) malloc(sizeof(*data) *NUM_FEATURES * NUM_TRAINING);
  LabelType *label = (LabelType *) malloc(sizeof(*label) * NUM_TRAINING);
  FeatureType *theta = (FeatureType *)malloc(sizeof(*theta) * NUM_FEATURES);

  int N = NUM_FEATURES * NUM_TRAINING;
  for(int i=0; i<N; i++){
    data[i] =  i%N;
  }
  for(int i=0; i<NUM_TRAINING; i++){
    label[i] =  i%NUM_TRAINING;
  }
  for(int i=0; i<NUM_FEATURES; i++){
    theta[i] =  i%NUM_FEATURES;
  }
  SgdLR_sw(data,label,theta);
}