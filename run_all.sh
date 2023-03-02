#!/bin/bash
echo "GRASP0 SHA"
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o GRASP0_SHA_2h_preTrained -args 0 SHA_MODEL
mv ./GRASP0_SHA_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP0_SHA_2h" ]; then 
    mkdir ./saves/GRASP0_SHA_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP0_SHA_2h

echo "GRASP0 GSM"
python3 main.py -c ./benchmarks/gsm/add.c ./benchmarks/gsm/gsm.c ./benchmarks/gsm/lpc.c -d gsm.json -p Gsm_LPC_Analysis -o GRASP0_GSM_2h_preTrained -args 0 GSM_MODEL
mv ./GRASP0_GSM_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP0_GSM_2h" ]; then 
    mkdir ./saves/GRASP0_GSM_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP0_GSM_2h

echo "GRASP0 AES"
python3 main.py -c ./benchmarks/aes/aes_dec.c ./benchmarks/aes/aes_enc.c ./benchmarks/aes/aes.c ./benchmarks/aes/aes_func.c ./benchmarks/aes/aes_key.c -d aes.json -p aes_main -o GRASP0_AES_2h_preTrained -args 0 AES_MODEL
mv ./GRASP0_AES_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP0_AES_2h" ]; then 
    mkdir ./saves/GRASP0_AES_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP0_AES_2h
echo "GRASP0 DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o GRASP0_DIGIT_2h_preTrained -args 0 DIGIT_MODEL
mv ./GRASP0_DIGIT_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP0_DIGIT_2h" ]; then 
    mkdir ./saves/GRASP0_DIGIT_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP0_DIGIT_2h

echo "GRASP1 SHA"
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o GRASP1_SHA_2h_preTrained -args 1 SHA_MODEL
mv ./GRASP1_SHA_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP1_SHA_2h" ]; then 
    mkdir ./saves/GRASP1_SHA_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP1_SHA_2h

echo "GRASP1 GSM"
python3 main.py -c ./benchmarks/gsm/add.c ./benchmarks/gsm/gsm.c ./benchmarks/gsm/lpc.c -d gsm.json -p Gsm_LPC_Analysis -o GRASP1_GSM_2h_preTrained -args 1 GSM_MODEL
mv ./GRASP1_GSM_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP1_GSM_2h" ]; then 
    mkdir ./saves/GRASP1_GSM_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP1_GSM_2h
echo "GRASP1 AES"
python3 main.py -c ./benchmarks/aes/aes_dec.c ./benchmarks/aes/aes_enc.c ./benchmarks/aes/aes.c ./benchmarks/aes/aes_func.c ./benchmarks/aes/aes_key.c -d aes.json -p aes_main -o GRASP1_AES_2h_preTrained -args 1 AES_MODEL
mv ./GRASP1_AES_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP1_AES_2h" ]; then 
    mkdir ./saves/GRASP1_AES_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP1_AES_2h
echo "GRASP1 DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o GRASP1_DIGIT_2h_preTrained -args 1 DIGIT_MODEL
mv ./GRASP1_DIGIT_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP1_DIGIT_2h" ]; then 
    mkdir ./saves/GRASP1_DIGIT_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP1_DIGIT_2h

echo "GRASP2 SHA"
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o GRASP2_SHA_2h_preTrained -args 2 SHA_MODEL
mv ./GRASP2_SHA_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP2_SHA_2h" ]; then 
    mkdir ./saves/GRASP2_SHA_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP2_SHA_2h

echo "GRASP2 GSM"
python3 main.py -c ./benchmarks/gsm/add.c ./benchmarks/gsm/gsm.c ./benchmarks/gsm/lpc.c -d gsm.json -p Gsm_LPC_Analysis -o GRASP2_GSM_2h_preTrained -args 2 GSM_MODEL
mv ./GRASP2_GSM_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP2_GSM_2h" ]; then 
    mkdir ./saves/GRASP2_GSM_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP2_GSM_2h
echo "GRASP2 AES"
python3 main.py -c ./benchmarks/aes/aes_dec.c ./benchmarks/aes/aes_enc.c ./benchmarks/aes/aes.c ./benchmarks/aes/aes_func.c ./benchmarks/aes/aes_key.c -d aes.json -p aes_main -o GRASP2_AES_2h_preTrained -args 2 AES_MODEL
mv ./GRASP2_AES_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP2_AES_2h" ]; then 
    mkdir ./saves/GRASP2_AES_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP2_AES_2h
echo "GRASP2 DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o GRASP2_DIGIT_2h_preTrained -args 2 DIGIT_MODEL
mv ./GRASP2_DIGIT_2h_preTrained ./dse/
if [ ! -d "./saves/GRASP2_DIGIT_2h" ]; then 
    mkdir ./saves/GRASP2_DIGIT_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/GRASP2_DIGIT_2h


echo "Genetic SHA"
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o genetic_SHA_2h_preTrained -args -1 SHA_MODEL
mv ./genetic_SHA_2h_preTrained ./dse/
if [ ! -d "./saves/genetic_SHA_2h" ]; then 
    mkdir ./saves/genetic_SHA_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/genetic_SHA_2h

echo "genetic GSM"
python3 main.py -c ./benchmarks/gsm/add.c ./benchmarks/gsm/gsm.c ./benchmarks/gsm/lpc.c -d gsm.json -p Gsm_LPC_Analysis -o genetic_GSM_2h_preTrained -args -1 GSM_MODEL
mv ./genetic_GSM_2h_preTrained ./dse/
if [ ! -d "./saves/genetic_GSM_2h" ]; then 
    mkdir ./saves/genetic_GSM_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/genetic_GSM_2h
echo "genetic AES"
python3 main.py -c ./benchmarks/aes/aes_dec.c ./benchmarks/aes/aes_enc.c ./benchmarks/aes/aes.c ./benchmarks/aes/aes_func.c ./benchmarks/aes/aes_key.c -d aes.json -p aes_main -o genetic_AES_2h_preTrained -args -1 AES_MODEL
mv ./genetic_AES_2h_preTrained ./dse/
if [ ! -d "./saves/genetic_AES_2h" ]; then 
    mkdir ./saves/genetic_AES_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/genetic_AES_2h
echo "genetic DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o genetic_DIGIT_2h_preTrained -args -1 DIGIT_MODEL
mv ./genetic_DIGIT_2h_preTrained ./dse/
if [ ! -d "./saves/genetic_DIGIT_2h" ]; then 
    mkdir ./saves/genetic_DIGIT_2h
fi
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./saves/genetic_DIGIT_2h

