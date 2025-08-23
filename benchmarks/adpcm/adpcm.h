#ifndef ADPCM_H
#define ADPCM_H

#define SIZE 100

void adpcm_main(
    const int in_data[SIZE], 
    int encoded[SIZE/2], 
    int decoded[SIZE]
);

#endif // ADPCM_H