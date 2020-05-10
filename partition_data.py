import pandas as pd

# set dev and test set size
dev_size = 5000
test_size = 5000

data = pd.read_csv('nyt-ingredients-snapshot-2015.csv')

# grab random test set
test = data.sample(n=test_size)
data = data.drop(test.index)

# grab random dev set from remaining data
dev = data.sample(n=dev_size)
data = data.drop(dev.index)

# remaining data is allocated to the train set
train = data

# save all data down
test.to_csv('./data/test.csv')
dev.to_csv('./data/dev.csv')
train.to_csv('./data/train.csv')