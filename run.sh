#!/bin/bash

#ACO
# echo "ACO SHA"
# python3 main.py ACO -b SHA -o ACO_SHA2h_preTrained -t 7200 -model ./models/SHA_MODEL
# # mv ./ACO_SHA2h_preTrained ./dse/
# if [ ! -d "./saves/ACO_SHA_2h" ]; then 
#     mkdir ./saves/ACO_SHA_2h
# fi
# mv ./time_stamps/* ./saves/ACO_SHA_2h/

echo "ACO GSM"
python3 main.py ACO -b GSM -o ACO_GSM2h_preTrained -t 7200 -model ./models/GSM_MODEL
# mv ./ACO_GSM2h_preTrained ./dse/
if [ ! -d "./saves/ACO_GSM_2h" ]; then 
    mkdir ./saves/ACO_GSM_2h
fi
mv ./time_stamps/* ./saves/ACO_GSM_2h/

# echo "ACO ADPCM"
# python3 main.py ACO -b ADPCM -o ACO_ADPCM2h_preTrained -t 7200 -model ./models/ADPCM_MODEL
# # mv ./ACO_ADPCM2h_preTrained ./dse/
# if [ ! -d "./saves/ACO_ADPCM_2h" ]; then 
#     mkdir ./saves/ACO_ADPCM_2h
# fi
# mv ./time_stamps/* ./saves/ACO_ADPCM_2h/

# echo "ACO AES"
# python3 main.py ACO -b AES -o ACO_AES2h_preTrained -t 7200 -model ./models/AES_MODEL
# # mv ./ACO_AES2h_preTrained ./dse/
# if [ ! -d "./saves/ACO_AES_2h" ]; then 
#    mkdir ./saves/ACO_AES_2h
# fi
# mv ./time_stamps/* ./saves/ACO_AES_2h/

#genetic
# echo "GENETIC SHA"
# python3 main.py genetic -b SHA -o genetic_SHA2h_preTrained -t 7200 -model ./models/SHA_MODEL
# mv ./genetic_SHA2h_preTrained ./dse/
# if [ ! -d "./saves/genetic_SHA_2h" ]; then 
#     mkdir ./saves/genetic_SHA_2h
# fi
# mv ./time_stamps/* ./saves/genetic_SHA_2h/

# echo "GENETIC GSM"
# python3 main.py genetic -b GSM -o genetic_GSM2h_preTrained -t 7200 -model ./models/GSM_MODEL
# mv ./genetic_GSM2h_preTrained ./dse/
# if [ ! -d "./saves/genetic_GSM_2h" ]; then 
#     mkdir ./saves/genetic_GSM_2h
# fi
# mv ./time_stamps/* ./saves/genetic_GSM_2h/

# echo "GENETIC ADPCM"
# python3 main.py genetic -b ADPCM -o genetic_ADPCM2h_preTrained -t 7200 -model ./models/ADPCM_MODEL
# mv ./genetic_ADPCM2h_preTrained ./dse/
# if [ ! -d "./saves/genetic_ADPCM_2h" ]; then 
#     mkdir ./saves/genetic_ADPCM_2h
# fi
# mv ./time_stamps/* ./saves/genetic_ADPCM_2h/

# echo "GENETIC AES"
# python3 main.py genetic -b AES -o genetic_AES2h_preTrained -t 7200 -model ./models/AES_MODEL
# mv ./genetic_AES2h_preTrained ./dse/
# if [ ! -d "./saves/genetic_AES_2h" ]; then 
#    mkdir ./saves/genetic_AES_2h
# fi
# mv ./time_stamps/* ./saves/genetic_AES_2h/

# echo "GRASP SHA"
# python3 main.py GRASP -b SHA -o GRASP_SHA2h_preTrained -t 7200 -model ./models/SHA_MODEL
# mv ./GRASP_SHA2h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_SHA_2h" ]; then 
#     mkdir ./saves/GRASP_SHA_2h
# fi
# mv ./time_stamps/* ./saves/GRASP_SHA_2h/

# echo "GRASP GSM"
# python3 main.py GRASP -b GSM -o GRASP_GSM2h_preTrained -t 7200 -model ./models/GSM_MODEL
# mv ./GRASP_GSM2h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_GSM_2h" ]; then 
#     mkdir ./saves/GRASP_GSM_2h
# fi
# mv ./time_stamps/* ./saves/GRASP_GSM_2h/

# echo "GRASP ADPCM"
# python3 main.py GRASP -b ADPCM -o GRASP_ADPCM2h_preTrained -t 7200 -model ./models/ADPCM_MODEL
# mv ./GRASP_ADPCM2h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_ADPCM_2h" ]; then 
#     mkdir ./saves/GRASP_ADPCM_2h
# fi
# mv ./time_stamps/* ./saves/GRASP_ADPCM_2h/

# echo "GRASP AES"
# python3 main.py GRASP -b AES -o GRASP_AES2h_preTrained -t 7200 -model ./models/AES_MODEL
# mv ./GRASP_AES2h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_AES_2h" ]; then 
#    mkdir ./saves/GRASP_AES_2h
# fi
# mv ./time_stamps/* ./saves/GRASP_AES_2h/