#!/bin/bash

URL="https://jina-examples-datasets.s3.amazonaws.com/memes/memes.json"
OUTPUT_DIR="./data2"
OUTPUT_FILENAME=$OUTPUT_DIR/memes.json

mkdir -p $OUTPUT_DIR

wget -O $OUTPUT_FILENAME $URL
