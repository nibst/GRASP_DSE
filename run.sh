#!/bin/bash
echo "SOFT GRASP GSM"
python3 main.py SOFT_PRUNING_GRASP -b GSM -o SOFT_PRUNING_GRASP_GSM2h_preTrained -t 7200 -model ./models/GSM_MODEL
mv ./SOFT_PRUNING_GRASP_GSM2h_preTrained ./dse/
if [ ! -d "./saves/SOFT_PRUNING_GRASP_GSM_2h" ]; then 
    mkdir ./saves/SOFT_PRUNING_GRASP_GSM_2h
fi
echo "SOFT GRASP SHA"
python3 main.py SOFT_PRUNING_GRASP -b SHA -o SOFT_PRUNING_GRASP_SHA2h_preTrained -t 7200 -model ./models/SHA_MODEL
mv ./SOFT_PRUNING_GRASP_SHA2h_preTrained ./dse/
if [ ! -d "./saves/SOFT_PRUNING_GRASP_SHA_2h" ]; then 
    mkdir ./saves/SOFT_PRUNING_GRASP_SHA_2h
fi
echo "SOFT GRASP AES"
python3 main.py SOFT_PRUNING_GRASP -b AES -o SOFT_PRUNING_GRASP_AES2h_preTrained -t 7200 -model ./models/AES_MODEL
mv ./SOFT_PRUNING_GRASP_AES2h_preTrained ./dse/
if [ ! -d "./saves/SOFT_PRUNING_GRASP_AES_2h" ]; then 
    mkdir ./saves/SOFT_PRUNING_GRASP_AES_2h
fi
echo "SOFT GRASP ADPCM"
python3 main.py SOFT_PRUNING_GRASP -b ADPCM -o SOFT_PRUNING_GRASP_ADPCM2h_preTrained -t 7200 -model ./models/ADPCM_MODEL
mv ./SOFT_PRUNING_GRASP_ADPCM2h_preTrained ./dse/
if [ ! -d "./saves/SOFT_PRUNING_GRASP_ADPCM_2h" ]; then 
    mkdir ./saves/SOFT_PRUNING_GRASP_ADPCM_2h
fi

