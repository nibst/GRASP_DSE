#!/bin/bash
echo "GRASP1 DIGIT"
python3 main.py -c ./benchmarks/digit-recognition/src/sw/digitrec_sw.cpp -d digit_recognition.json -p DigitRec_sw -o GRASP1_DIGIT_2h_teste -args 1 DIGIT_MODEL

