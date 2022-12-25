#!/bin/sh
echo "GRASP1 SHA"
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o GRASP1_SHA_10h_3h -args 1
mv ./GRASP1_SHA_10h_3h ./dse/
if [ ! -d "./time_stamps/GRASP1_SHA" ] then 
    mkdir ./time_stamps/GRASP1_SHA
fi
#To move all files, but not folders: 
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_SHA 
echo "GRASP1 GSM"
python3 main.py -c ./benchmarks/gsm/add.c ./benchmarks/gsm/gsm.c ./benchmarks/gsm/lpc.c -d gsm.json -p Gsm_LPC_Analysis -o GRASP1_GSM_10h_3h -args 1
mv ./GRASP1_GSM_10h_3h ./dse/
if [ ! -d "./time_stamps/GRASP1_GSM" ]; then 
    mkdir ./time_stamps/GRASP1_GSM
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_GSM

echo "GRASP1 AES"
python3 main.py -c ./benchmarks/aes/aes_dec.c ./benchmarks/aes/aes_enc.c ./benchmarks/aes/aes.c ./benchmarks/aes/aes_func.c ./benchmarks/aes/aes_key.c -d aes.json -p aes_main -o GRASP1_AES_10h_3h -args 1
mv ./GRASP1_AES_10h_3h ./dse/
if [ ! -d "./time_stamps/GRASP1_AES" ]; then 
    mkdir ./time_stamps/GRASP1_AES
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_AES

echo "GRASP1 DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o GRASP1_DIGIT_10h_3h -args 1
mv ./GRASP1_DIGIT_10h_3h ./dse/
if [ ! -d "./time_stamps/GRASP1_DIGIT" ]; then 
    mkdir ./time_stamps/GRASP1_DIGIT
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_DIGIT

echo "GRASP0 SHA"
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o GRASP0_SHA_10h_3h -args 0
mv ./GRASP0_SHA_10h_3h ./dse/
if [ ! -d "./time_stamps/GRASP0_SHA" ]; then 
    mkdir ./time_stamps/GRASP0_SHA
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP0_SHA

echo "GRASP0 DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o GRASP0_DIGIT_10h_3h -args 0
mv ./GRASP0_DIGIT_10h_3h ./dse/
if [ ! -d "./time_stamps/GRASP0_DIGIT" ]; then 
    mkdir ./time_stamps/GRASP0_DIGIT
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP0_DIGIT