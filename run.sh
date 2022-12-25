#!/bin/sh
python3 main.py -c ./benchmarks/sha/sha.c ./benchmarks/sha/sha_driver.c -d sha.json -p sha_stream -o GRASP1_SHA_10h_3h
mv ./GRASP1_SHA_10h_3h ./dse/
#To move all files, but not folders: 
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_SHA 

python3 main.py -c ./benchmarks/gsm/add.c ./benchmarks/gsm/gsm.c ./benchmarks/gsm/lpc.c -d gsm.json -p Gsm_LPC_Analysis -o GRASP1_GSM_10h_3h    
mv ./GRASP1_GSM_10h_3h ./dse/
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_GSM


python3 main.py -c ./benchmarks/aes/aes_dec.c ./benchmarks/aes/aes_enc.c ./benchmarks/aes/aes.c ./benchmarks/aes/aes_func.c ./benchmarks/aes/aes_key.c -d aes.json -p aes_main -o GRASP1_AES_10h_3h
mv ./GRASP1_AES_10h_3h ./dse/
find ./time_stamps/ -type f -print0 | xargs -0 mv -t ./time_stamps/GRASP1_AES

