#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <math.h>
#include <stdbool.h>

typedef struct BinOpInfo{
  uint32_t opID; 
  uint32_t opCode;
  bool isSignedValue;
  bool isFpValue;
  uint32_t bitwidth;
  double numOccurs;
  double mean;
  double variance;
  double standardDev;
  double sumOfSquares;
  struct BinOpInfo* next;
   
} BinOpInfo;

BinOpInfo* ops = NULL;

void profOp(uint64_t instID, uint8_t instOpcode, int64_t signedIntValue, uint64_t unsignedIntValue, 
            double fpValue, bool isSignedValue, bool isFpValue, uint32_t bitwidth) {
      
      bool isNewOp = true;
      BinOpInfo* currentOp = ops;
      while(currentOp != NULL){
          if(currentOp->opID == instID){
              double oldNumOccurs = currentOp->numOccurs; 
              double oldMean = currentOp->mean;
              double oldVariance = currentOp->variance;
              double newNumOccurs = oldNumOccurs + 1;
              double squaredValue;
              double newMean;
              double newVariance;
              
              if(isFpValue){
                  squaredValue = pow(fpValue, 2);
                  newMean = oldMean + ((fpValue - oldMean) / newNumOccurs); 
                  newVariance = ((oldNumOccurs/newNumOccurs) * oldVariance) + 
                                (((fpValue - oldMean) / newNumOccurs) * (fpValue - newMean)); 
              }
              else{
                  if(isSignedValue){
                      squaredValue = pow(signedIntValue, 2);
                      newMean = oldMean + ((signedIntValue - oldMean) / newNumOccurs); 
                      newVariance = ((oldVariance / newNumOccurs) * oldNumOccurs) + 
                                    (((newMean - signedIntValue) / newNumOccurs) * (newMean - signedIntValue)); 
                  }
                  else{
                     squaredValue = pow(unsignedIntValue, 2);
                     newMean = oldMean + ((unsignedIntValue - oldMean) / newNumOccurs); 
                     newVariance = ((oldVariance / newNumOccurs) * oldNumOccurs) + 
                                    (((newMean - unsignedIntValue) / newNumOccurs) * (newMean - unsignedIntValue));  
                  }         
              }
              currentOp->numOccurs = newNumOccurs; 
              currentOp->mean = newMean;
              currentOp->variance = newVariance;
              currentOp->standardDev = sqrt(newVariance);
              currentOp->sumOfSquares += squaredValue;
              isNewOp = false;
              break;  
          }
          else{
              currentOp = currentOp->next; 
          }
      }
      if(isNewOp){
         BinOpInfo* newOp = malloc(sizeof(BinOpInfo));
         newOp->opID = (uint32_t)instID;
         newOp->opCode = instOpcode;
         newOp->numOccurs = 1;
         if(isFpValue){
             newOp->mean = fpValue;
             newOp->sumOfSquares = pow(fpValue, 2);
         }
         else{ 
             if(isSignedValue){ 
                newOp->mean = signedIntValue;
                newOp->sumOfSquares = pow(signedIntValue, 2);
             }
             else{
                newOp->mean = unsignedIntValue;
                newOp->sumOfSquares = pow(unsignedIntValue, 2);
             }
         }
         newOp->isSignedValue = isSignedValue;
         newOp->isFpValue = isFpValue; 
         newOp->bitwidth = bitwidth;
         newOp->variance = 0;
         newOp->standardDev = 0;
         newOp->next = ops;
         ops = newOp;
              
      } 
}

void saveProfile(const char *fileName) {
     int count = 0;
     BinOpInfo* nextOp;
     FILE* outputFile = fopen(fileName, "w");
     if(outputFile){
         while(ops != NULL){
        //OPID | OPCode | isSignedValue | isFloatingPointValue | bitwidth | numOccurs | mean | variance | standardDev | sumOfSquares 
            fprintf (outputFile, "%"PRIu32"|%"PRIu32"|%"PRIu32"|%"PRIu32"|%"PRIu32"|%"PRIu32"|%lf|%lf|%lf|%lf|\n", 
                    ops->opID, ops->opCode, (uint32_t)ops->isSignedValue, (uint32_t)ops->isFpValue, 
                    ops->bitwidth, (uint32_t)ops->numOccurs, ops->mean, ops->variance, ops->standardDev, ops->sumOfSquares); 
            nextOp = ops->next;
            free(ops);
            ops = nextOp;
            count++;
         }
         fclose(outputFile);  
     }
     else
         printf("Unable to open %s\n", fileName);
     
}


