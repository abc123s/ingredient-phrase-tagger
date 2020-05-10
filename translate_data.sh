#!/bin/bash

# convert training data to crf++ format
bin/generate_data \
  --data-path="./data/train.csv" > "./data/train.crf"

# convert dev data to crf++ format
bin/generate_data \
  --data-path="./data/dev.csv" > "./data/dev.crf"

# convert test data to crf++ format
bin/generate_data \
  --data-path="./data/test.csv" > "./data/test.crf"
