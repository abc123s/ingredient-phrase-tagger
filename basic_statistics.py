import pandas as pd

from ingredient_phrase_tagger.training import tokenizer, translator, utils

data = pd.read_csv('nyt-ingredients-snapshot-2015.csv')

output = open('./basic_statistics.txt', 'w')

# print total number of sentences in our data set
output.write('# of sentences:\n')
output.write(str(len(data.index)))
output.write('\n\n')

data = data.fillna('')

# modified version of _bestTag in translator, since 
# I'm not performing BIO tagging right now
def best_tag(tags):
    if len(tags) == 1:
        return tags[0]

    # if there are multiple tags, pick the first which isn't COMMENT
    else:
        for t in tags:
            if (t != "COMMENT") and (t != "COMMENT"):
                return t

    # we have no idea what to guess
    return "OTHER"

#count tokens and tags
token_count = 0
tag_count = {}
for index, row in data.iterrows():
    # clean and tokenize raw sentence / ingredient phrase
    raw = utils.cleanUnicodeFractions(row['input'].decode('utf-8'))
    tokens = tokenizer.tokenize(raw)

    # match tokens to labels and count labels
    labels = translator._row_to_labels(row)
    for token in tokens:
        # count tokens
        token_count += 1

        # compute tag
        possible_tags = translator._matchUp(token, labels)
        tag = best_tag(possible_tags)
        
        # count tags
        tag_count[tag] = tag_count[tag] + 1 if tag in tag_count else 1

# print total number of tokens in our data set
output.write('# of tokens:\n')
output.write(str(token_count))
output.write('\n\n')

# print distribution of tags in our data set
output.write('# of tags:\n')
output.write(str(tag_count))
output.write('\n\n')



