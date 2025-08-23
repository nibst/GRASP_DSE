#!/bin/bash
source .venv/bin/activate

echo "KNN"
python3 main.py GRASP  -o out -b KNN -t 10 -model ./models/KNN_MODEL

# echo "GSM"
# python3 main.py GRASP  -o out -b GSM -t 10 -model ./models/GSM_MODEL
