from English_preprocess import *
from Persian_preprocess import *
from IndexConstruction import *
from IndexCompression import *
import pandas as pd
import ast
from xml.dom import minidom

# Step 1: Preprocess

data = pd.read_csv("data/ted_talks.csv")
tokenized_lemmatized = prepare_text_english(data)
tokenized_lemmatized_removed_stop_words = remove_stop_words_english(tokenized_lemmatized)
merged_id_english = add_id_english(tokenized_lemmatized_removed_stop_words)
with open('data/tedTalk_Preprocessed.txt', 'w', encoding='utf-8') as f:
    for page in merged_id_english:
        f.write("%s\n" % page)

mydoc = minidom.parse('data/Persian.xml')
items_text = mydoc.getElementsByTagName('text')
pages_text_data = [items_text[i].firstChild.data for i in range(len(items_text))]
text_tokenized_lemmatized_pages = prepare_text_persian(pages_text_data)
text_tokenized_lemmatized_removed_stop_words_pages = remove_stopwords_persian(text_tokenized_lemmatized_pages)
items_title = mydoc.getElementsByTagName('title')
pages_title_data = [items_title[i].firstChild.data for i in range(len(items_title))]
title_tokenized_lemmatized_pages = prepare_text_persian(pages_title_data)
title_tokenized_lemmatized_removed_stop_words_pages = remove_stopwords_persian(title_tokenized_lemmatized_pages)
merged_id_text_title = merge_text_title_and_add_id_persian(title_tokenized_lemmatized_removed_stop_words_pages,
                                                           text_tokenized_lemmatized_removed_stop_words_pages)
with open('data/persian_preProcessed.txt', 'w', encoding='utf-8') as f:
    for page in merged_id_text_title:
        f.write("%s\n" % page)

# Step 2: Index Construction
tedTalk_preProcessed = []
with open('data/tedTalk_Preprocessed.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
for line in lines:
    tedTalk_preProcessed.append(list(ast.literal_eval(line)))
pos_index_tedtalks, bigram_index_tedtalks = construct_index(tedTalk_preProcessed)
write_index_to_file(pos_index_tedtalks, "data/positional_index_tedTalks.pkl")
write_index_to_file(bigram_index_tedtalks, "data/bigram_index_tedTalks.pkl")

persian_preProcessed = []
with open('data/persian_preProcessed.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
for line in lines:
    persian_preProcessed.append(list(ast.literal_eval(line)))
pos_index_persian, bigram_index_persian = construct_index(persian_preProcessed)
write_index_to_file(pos_index_persian, "data/positional_index_persian.pkl")
write_index_to_file(bigram_index_persian, "data/bigram_index_persian.pkl")

# Step 3: Index Compression
positional_index_tedTalks = read_index_from_file("data/positional_index_tedTalks.pkl")

vb_tedTalks = VariableByteCode(positional_index_tedTalks)
vb_tedTalks.compress()
vb_tedTalks.decompress()
print("result of Variable Bytes encoding for Ted Talks:")
vb_tedTalks.compare()
write_index_to_file(vb_tedTalks.compressed, "data/positional_index_tedTalks_vb.pkl")

gamma_tedTalks = GammaCode(positional_index_tedTalks)
gamma_tedTalks.compress()
gamma_tedTalks.decompress()
print("result of Gamma encoding for Ted Talks:")
gamma_tedTalks.compare()
write_index_to_file(gamma_tedTalks.compressed, "data/positional_index_tedTalks_gamma.pkl")


positional_index_persian = read_index_from_file("data/positional_index_persian.pkl")

vb_persian = VariableByteCode(positional_index_persian)
vb_persian.compress()
vb_persian.decompress()
print("result of Variable Bytes encoding for persian XMLs:")
vb_persian.compare()
write_index_to_file(vb_persian.compressed, "data/positional_index_persian_vb.pkl")

gamma_persian = GammaCode(positional_index_persian)
gamma_persian.compress()
gamma_persian.decompress()
print("result of Gamma encoding encoding for persian XMLs:")
gamma_persian.compare()
write_index_to_file(gamma_persian.compressed, "data/positional_index_persian_gamma.pkl")


# step 4 (query correction):
#   input: a query string + bigram index + positional index
#   output: corrected query :D

# step 5 (document retrieval):
#   input: a query string
#   output: list of documents :-? do you only show IDs? do you print out the documents :-? ????
