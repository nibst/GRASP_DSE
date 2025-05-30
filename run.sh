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

# echo "GRASP SHA"
# python3 main.py GRASP -b SHA -o GRASP_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL
# mv ./GRASP_SHA4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_SHA_4h" ]; then 
#    mkdir ./saves/GRASP_SHA_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_SHA_4h/

# echo "GRASP GSM"
# python3 main.py GRASP -b GSM -o GRASP_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL
# mv ./GRASP_GSM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_GSM_4h" ]; then 
#    mkdir ./saves/GRASP_GSM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_GSM_4h/

# echo "GRASP ADPCM"
# python3 main.py GRASP -b ADPCM -o GRASP_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL
# mv ./GRASP_ADPCM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_ADPCM_4h" ]; then 
#     mkdir ./saves/GRASP_ADPCM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_ADPCM_4h/

# echo "GRASP AES"
# python3 main.py GRASP -b AES -o GRASP_AES4h_preTrained -t 14400 -model ./models/AES_MODEL
# mv ./GRASP_AES4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_AES_4h" ]; then 
#   mkdir ./saves/GRASP_AES_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_AES_4h/

# echo "GRASP GEMM"
# python3 main.py GRASP -b GEMM -o GRASP_GEMM4h_preTrained -t 14400 -model ./models/GEMM_MODEL
# mv ./GRASP_GEMM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_GEMM_4h" ]; then 
#   mkdir ./saves/GRASP_GEMM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_GEMM_4h/

# echo "GRASP KNN"
# python3 main.py GRASP -b KNN -o GRASP_KNN4h_preTrained -t 14400 -model ./models/KNN_MODEL
# mv ./GRASP_KNN4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_KNN_4h" ]; then 
#  mkdir ./saves/GRASP_KNN_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_KNN_4h/
echo "GRASP TRANS_FFT"
python3 main.py GRASP -b TRANS_FFT -o GRASP_TRANS_FFT4h_preTrained -t 14400 -model ./models/TRANS_FFT_MODEL
mv ./GRASP_TRANS_FFT4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_TRANS_FFT_4h" ]; then 
  mkdir ./saves/GRASP_TRANS_FFT_4h
fi
mv ./time_stamps/* ./saves/GRASP_TRANS_FFT_4h/
# Period explored at the start   ------------------------------------------------------------------------------------------

# echo "GRASP_FREQUENCY SHA"
# python3 main.py GRASP_FREQUENCY -b SHA -o GRASP_FREQUENCY_start_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL -args start
# mv ./GRASP_FREQUENCY_start_SHA4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_start_SHA_4h" ]; then 
#    mkdir ./saves/GRASP_FREQUENCY_start_SHA_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_SHA_4h/

# echo "GRASP_FREQUENCY GSM"
# python3 main.py GRASP_FREQUENCY -b GSM -o GRASP_FREQUENCY_start_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL -args start
# mv ./GRASP_FREQUENCY_start_GSM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_start_GSM_4h" ]; then 
#    mkdir ./saves/GRASP_FREQUENCY_start_GSM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_GSM_4h/

# echo "GRASP_FREQUENCY ADPCM"
# python3 main.py GRASP_FREQUENCY -b ADPCM -o GRASP_FREQUENCY_start_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL -args start
# mv ./GRASP_FREQUENCY_start_ADPCM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_start_ADPCM_4h" ]; then 
#     mkdir ./saves/GRASP_FREQUENCY_start_ADPCM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_ADPCM_4h/

# echo "GRASP_FREQUENCY AES"
# python3 main.py GRASP_FREQUENCY -b AES -o GRASP_FREQUENCY_start_AES4h_preTrained -t 14400 -model ./models/AES_MODEL -args start
# mv ./GRASP_FREQUENCY_start_AES4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_start_AES_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_start_AES_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_AES_4h/


# echo "GRASP_FREQUENCY GEMM"
# python3 main.py GRASP_FREQUENCY -b GEMM -o GRASP_FREQUENCY_start_GEMM4h_preTrained -t 14400 -model ./models/GEMM_MODEL -args start
# mv ./GRASP_FREQUENCY_start_GEMM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_start_GEMM_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_start_GEMM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_GEMM_4h/


# echo "GRASP_FREQUENCY KNN"
# python3 main.py GRASP_FREQUENCY -b KNN -o GRASP_FREQUENCY_start_KNN4h_preTrained -t 14400 -model ./models/KNN_MODEL -args start
# mv ./GRASP_FREQUENCY_start_KNN4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_start_KNN_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_start_KNN_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_KNN_4h/

echo "GRASP_FREQUENCY TRANS_FFT"
python3 main.py GRASP_FREQUENCY -b TRANS_FFT -o GRASP_FREQUENCY_start_TRANS_FFT4h_preTrained -t 14400 -model ./models/TRANS_FFT_MODEL -args start
mv ./GRASP_FREQUENCY_start_TRANS_FFT4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_FREQUENCY_start_TRANS_FFT_4h" ]; then 
  mkdir ./saves/GRASP_FREQUENCY_start_TRANS_FFT_4h
fi
mv ./time_stamps/* ./saves/GRASP_FREQUENCY_start_TRANS_FFT_4h/

# Period explored at the middle ------------------------------------------------------------------------------------------
# echo "GRASP_FREQUENCY SHA"
# python3 main.py GRASP_FREQUENCY -b SHA -o GRASP_FREQUENCY_mid_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL -args mid
# mv ./GRASP_FREQUENCY_mid_SHA4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_mid_SHA_4h" ]; then 
#    mkdir ./saves/GRASP_FREQUENCY_mid_SHA_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_SHA_4h/

# echo "GRASP_FREQUENCY GSM"
# python3 main.py GRASP_FREQUENCY -b GSM -o GRASP_FREQUENCY_mid_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL -args mid
# mv ./GRASP_FREQUENCY_mid_GSM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_mid_GSM_4h" ]; then 
#    mkdir ./saves/GRASP_FREQUENCY_mid_GSM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_GSM_4h/

# echo "GRASP_FREQUENCY ADPCM"
# python3 main.py GRASP_FREQUENCY -b ADPCM -o GRASP_FREQUENCY_mid_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL -args mid
# mv ./GRASP_FREQUENCY_mid_ADPCM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_mid_ADPCM_4h" ]; then 
#     mkdir ./saves/GRASP_FREQUENCY_mid_ADPCM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_ADPCM_4h/

# echo "GRASP_FREQUENCY AES"
# python3 main.py GRASP_FREQUENCY -b AES -o GRASP_FREQUENCY_mid_AES4h_preTrained -t 14400 -model ./models/AES_MODEL -args mid
# mv ./GRASP_FREQUENCY_mid_AES4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_mid_AES_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_mid_AES_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_AES_4h/


# echo "GRASP_FREQUENCY GEMM"
# python3 main.py GRASP_FREQUENCY -b GEMM -o GRASP_FREQUENCY_mid_GEMM4h_preTrained -t 14400 -model ./models/GEMM_MODEL -args mid
# mv ./GRASP_FREQUENCY_mid_GEMM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_mid_GEMM_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_mid_GEMM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_GEMM_4h/
# echo "GRASP_FREQUENCY KNN"
# python3 main.py GRASP_FREQUENCY -b KNN -o GRASP_FREQUENCY_mid_KNN4h_preTrained -t 14400 -model ./models/KNN_MODEL -args mid
# mv ./GRASP_FREQUENCY_mid_KNN4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_mid_KNN_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_mid_KNN_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_KNN_4h/

echo "GRASP_FREQUENCY TRANS_FFT"
python3 main.py GRASP_FREQUENCY -b TRANS_FFT -o GRASP_FREQUENCY_mid_TRANS_FFT4h_preTrained -t 14400 -model ./models/TRANS_FFT_MODEL -args mid
mv ./GRASP_FREQUENCY_mid_TRANS_FFT4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_FREQUENCY_mid_TRANS_FFT_4h" ]; then 
  mkdir ./saves/GRASP_FREQUENCY_mid_TRANS_FFT_4h
fi
mv ./time_stamps/* ./saves/GRASP_FREQUENCY_mid_TRANS_FFT_4h/


# Period explored at the end   ------------------------------------------------------------------------------------------
# echo "GRASP_FREQUENCY SHA"
# python3 main.py GRASP_FREQUENCY -b SHA -o GRASP_FREQUENCY_end_SHA4h_preTrained -t 14400 -model ./models/SHA_MODEL -args end
# mv ./GRASP_FREQUENCY_end_SHA4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_end_SHA_4h" ]; then 
#    mkdir ./saves/GRASP_FREQUENCY_end_SHA_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_SHA_4h/

# echo "GRASP_FREQUENCY GSM"
# python3 main.py GRASP_FREQUENCY -b GSM -o GRASP_FREQUENCY_end_GSM4h_preTrained -t 14400 -model ./models/GSM_MODEL -args end
# mv ./GRASP_FREQUENCY_end_GSM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_end_GSM_4h" ]; then 
#    mkdir ./saves/GRASP_FREQUENCY_end_GSM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_GSM_4h/

# echo "GRASP_FREQUENCY ADPCM"
# python3 main.py GRASP_FREQUENCY -b ADPCM -o GRASP_FREQUENCY_end_ADPCM4h_preTrained -t 14400 -model ./models/ADPCM_MODEL -args end
# mv ./GRASP_FREQUENCY_end_ADPCM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_end_ADPCM_4h" ]; then 
#     mkdir ./saves/GRASP_FREQUENCY_end_ADPCM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_ADPCM_4h/

# echo "GRASP_FREQUENCY AES"
# python3 main.py GRASP_FREQUENCY -b AES -o GRASP_FREQUENCY_end_AES4h_preTrained -t 14400 -model ./models/AES_MODEL -args end
# mv ./GRASP_FREQUENCY_end_AES4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_end_AES_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_end_AES_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_AES_4h/


# echo "GRASP_FREQUENCY GEMM"
# python3 main.py GRASP_FREQUENCY -b GEMM -o GRASP_FREQUENCY_end_GEMM4h_preTrained -t 14400 -model ./models/GEMM_MODEL -args end
# mv ./GRASP_FREQUENCY_end_GEMM4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_end_GEMM_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_end_GEMM_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_GEMM_4h/

# echo "GRASP_FREQUENCY KNN"
# python3 main.py GRASP_FREQUENCY -b KNN -o GRASP_FREQUENCY_end_KNN4h_preTrained -t 14400 -model ./models/KNN_MODEL -args end
# mv ./GRASP_FREQUENCY_end_KNN4h_preTrained ./dse/
# if [ ! -d "./saves/GRASP_FREQUENCY_end_KNN_4h" ]; then 
#   mkdir ./saves/GRASP_FREQUENCY_end_KNN_4h
# fi
# mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_KNN_4h/

echo "GRASP_FREQUENCY TRANS_FFT"
python3 main.py GRASP_FREQUENCY -b TRANS_FFT -o GRASP_FREQUENCY_end_TRANS_FFT4h_preTrained -t 14400 -model ./models/TRANS_FFT_MODEL -args end
mv ./GRASP_FREQUENCY_end_TRANS_FFT4h_preTrained ./dse/
if [ ! -d "./saves/GRASP_FREQUENCY_end_TRANS_FFT_4h" ]; then 
  mkdir ./saves/GRASP_FREQUENCY_end_TRANS_FFT_4h
fi
mv ./time_stamps/* ./saves/GRASP_FREQUENCY_end_TRANS_FFT_4h/
# -----------------------------------------------------------------------------------------------------------------------------------------------

deactivate
