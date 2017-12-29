#!/bin/bash

OUT_FILE=uvindx_info_lambda.zip

rm -rf ./build
rm -f ./$OUT_FILE

pip install -r ./requirements.txt -t ./build/
pip install -t ./build/ ./

cp ./uvindx_info_lambda.py ./build/
cd ./build && zip -r ../$OUT_FILE ./*
