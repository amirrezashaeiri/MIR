from Phase1.English_preprocess import *
from Phase2.preprocess_phase2 import *

import pandas as pd
import ast
from xml.dom import minidom

# Step 1: Preprocess.

data = pd.read_csv("data/train.csv")
tokenized_lemmatized = prepare_text_english(data)
tokenized_lemmatized_removed_stop_words = remove_stop_words_english(tokenized_lemmatized)
merged_id_english = add_id_english(tokenized_lemmatized_removed_stop_words)
with open('data/train_preprocessed.txt', 'w', encoding='utf-8') as f:
    for page in merged_id_english:
        f.write("%s\n" % page)
# set labels for phase1 dataset in terms of their view
data = pd.read_csv("C:/Users/abahr/PycharmProjects/MIR/Phase1/data/ted_talks.csv")
tokenized_lemmatized = prepare_text_english(data)
tokenized_lemmatized_removed_stop_words = remove_stop_words_english(tokenized_lemmatized)
merged_id_english = add_id_english(tokenized_lemmatized_removed_stop_words)
with open('data/tedTalk_Preprocessed.txt', 'w', encoding='utf-8') as f:
    for page in merged_id_english:
        f.write("%s\n" % page)

labels = label(data)
with open('data/labels.txt', 'w', encoding='utf-8') as f:
    for label in labels:
        f.write("%s\n" % label)
with open('data/labels.txt', 'r', encoding='utf-8') as f:
    labels = [int(i.replace("\n", "")) for i in f.readlines()]
