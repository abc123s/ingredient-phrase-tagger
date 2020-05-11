MODEL_TIMESTAMP=$(date +%Y%m%d_%H%M)
DATA_VERSION="train.csv"
CODE_VERSION=$(git rev-parse --short HEAD)

CRF_MODEL_FILE="./models/baseline/${MODEL_TIMESTAMP}-${DATA_VERSION}-${CODE_VERSION}.crfmodel"

# train model
crf_learn \
  "template_file" "./data/train.crf" "$CRF_MODEL_FILE"

# test model against train set
crf_test \
  --model="$CRF_MODEL_FILE" \
  "./data/train.crf" > "./models/baseline/train_output"

# test model against dev set
crf_test \
  --model="$CRF_MODEL_FILE" \
  "./data/dev.crf" > "./models/baseline/dev_output"

# test model against test set
crf_test \
  --model="$CRF_MODEL_FILE" \
  "./data/test.crf" > "./models/baseline/test_output"

# compute word-level and sentence-level accuracy on train / dev / test 
python bin/evaluate.py "./models/baseline/train_output" > "./models/baseline/train_performance"
python bin/evaluate.py "./models/baseline/dev_output" > "./models/baseline/dev_performance"
python bin/evaluate.py "./models/baseline/test_output" > "./models/baseline/test_performance"
