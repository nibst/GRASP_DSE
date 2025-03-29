#!/bin/bash
source .venv/bin/activate
which python
#ACO
# echo "ACO SHA"
# python3 main.py ACO -b SHA -o ACO_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL
# mv ./ACO_SHA4h_preTrained ./dse/
# if [ ! -d "./saves/ACO_SHA_4h" ]; then 
#     mkdir ./saves/ACO_SHA_4h
# fi
# mv ./time_stamps/* ./saves/ACO_SHA_4h/

# echo "ACO GSM"
# python3 main.py ACO -b GSM -o ACO_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL
# mv ./ACO_GSM4h_preTrained ./dse/
# if [ ! -d "./saves/ACO_GSM_4h" ]; then 
#     mkdir ./saves/ACO_GSM_4h
# fi
# mv ./time_stamps/* ./saves/ACO_GSM_4h/

# echo "ACO ADPCM"
# python3 main.py ACO -b ADPCM -o ACO_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL
# mv ./ACO_ADPCM4h_preTrained ./dse/
# if [ ! -d "./saves/ACO_ADPCM_4h" ]; then 
#      mkdir ./saves/ACO_ADPCM_4h
# fi
# mv ./time_stamps/* ./saves/ACO_ADPCM_4h/

# echo "ACO AES"
# python3 main.py ACO -b AES -o ACO_AES4h_preTrained -t 14400 -model ./models/AES_MODEL
# mv ./ACO_AES4h_preTrained ./dse/
# if [ ! -d "./saves/ACO_AES_4h" ]; then 
#    mkdir ./saves/ACO_AES_4h
# fi
# mv ./time_stamps/* ./saves/ACO_AES_4h/

# # genetic
# echo "GENETIC SHA"
# python3 main.py genetic -b SHA -o genetic_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL
# mv ./genetic_SHA4h_preTrained ./dse/
# if [ ! -d "./saves/genetic_SHA_4h" ]; then 
#     mkdir ./saves/genetic_SHA_4h
# fi
# mv ./time_stamps/* ./saves/genetic_SHA_4h/

# echo "GENETIC GSM"
# python3 main.py genetic -b GSM -o genetic_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL
# mv ./genetic_GSM4h_preTrained ./dse/
# if [ ! -d "./saves/genetic_GSM_4h" ]; then 
#     mkdir ./saves/genetic_GSM_4h
# fi
# mv ./time_stamps/* ./saves/genetic_GSM_4h/

# echo "GENETIC ADPCM"
# python3 main.py genetic -b ADPCM -o genetic_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL
# mv ./genetic_ADPCM4h_preTrained ./dse/
# if [ ! -d "./saves/genetic_ADPCM_4h" ]; then 
#     mkdir ./saves/genetic_ADPCM_4h
# fi
# mv ./time_stamps/* ./saves/genetic_ADPCM_4h/

# echo "GENETIC AES"
# python3 main.py genetic -b AES -o genetic_AES4h_preTrained -t 14400 -model ./models/AES_MODEL
# mv ./genetic_AES4h_preTrained ./dse/
# if [ ! -d "./saves/genetic_AES_4h" ]; then 
#    mkdir ./saves/genetic_AES_4h
# fi
# mv ./time_stamps/* ./saves/genetic_AES_4h/

echo "GRASP SHA"
python3 main.py GRASP -b SHA -o GRASP_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL
mv ./GRASP_SHA4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_SHA_4h" ]; then 
   mkdir ./saves/GRASP_SHA_4h
fi
mv ./time_stamps/* ./saves/GRASP_SHA_4h/

echo "GRASP GSM"
python3 main.py GRASP -b GSM -o GRASP_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL
mv ./GRASP_GSM4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_GSM_4h" ]; then 
   mkdir ./saves/GRASP_GSM_4h
fi
mv ./time_stamps/* ./saves/GRASP_GSM_4h/

echo "GRASP ADPCM"
python3 main.py GRASP -b ADPCM -o GRASP_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL
mv ./GRASP_ADPCM4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_ADPCM_4h" ]; then 
    mkdir ./saves/GRASP_ADPCM_4h
fi
mv ./time_stamps/* ./saves/GRASP_ADPCM_4h/

echo "GRASP AES"
python3 main.py GRASP -b AES -o GRASP_AES4h_preTrained -t 14400 -model ./models/AES_MODEL
mv ./GRASP_AES4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_AES_4h" ]; then 
  mkdir ./saves/GRASP_AES_4h
fi
mv ./time_stamps/* ./saves/GRASP_AES_4h/

echo "GRASP KNN"
python3 main.py GRASP -b KNN -o GRASP_KNN4h_preTrained -t 14400 -model ./models/KNN_MODEL
mv ./GRASP_KNN4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_KNN_4h" ]; then 
  mkdir ./saves/GRASP_KNN_4h
fi
mv ./time_stamps/* ./saves/GRASP_KNN_4h/
deactivate
