from English_preprocess import *
from Persian_preprocess import *
import pandas as pd
#tedTalks
# data = pd.read_csv("C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/ted_talks.csv")
# tokenized_lemmatized=prepare_text_english(data)
# tokenized_lemmatized_removed_stop_words=remove_stop_words_english(tokenized_lemmatized)
# merged_id_english=add_id_english(tokenized_lemmatized_removed_stop_words)
# with open('C:/Users/abahr/PycharmProjects/MIR/data/tedTalk_Preprocessed.txt', 'w',encoding='utf-8') as f:
#         for page in merged_id_english:
#             f.write("%s\n" % page)
#

#Persian
from xml.dom import minidom

mydoc = minidom.parse('C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/Persian.xml')
items_text = mydoc.getElementsByTagName('text')

pages_text_data=[items_text[i].firstChild.data for i in range (len(items_text))]

text_tokenized_lemmatized_pages= prepare_text_persian(pages_text_data)
text_tokenized_lemmatized_removed_stop_words_pages=remove_stopwords_persian(text_tokenized_lemmatized_pages)

items_title = mydoc.getElementsByTagName('title')

pages_title_data=[items_title[i].firstChild.data for i in range (len(items_title))]

title_tokenized_lemmatized_pages= prepare_text_persian(pages_title_data)
title_tokenized_lemmatized_removed_stop_words_pages=remove_stopwords_persian(title_tokenized_lemmatized_pages)


merged_id_text_title=merge_text_title_and_add_id_persian(title_tokenized_lemmatized_removed_stop_words_pages,text_tokenized_lemmatized_removed_stop_words_pages)


with open('C:/Users/abahr/PycharmProjects/MIR/data/persian_preProcessed.txt', 'w',encoding='utf-8') as f:
    for page in merged_id_text_title:
        f.write("%s\n" % page)


#preprocess finished.. preprocess files are saved



#loading preprocessed files
with open('C:/Users/abahr/PycharmProjects/MIR/data/tedTalk_Preprocessed.txt',encoding='utf-8') as f:
    lines = f.read().splitlines()
tedTalk_preProcessed=[]
import ast
for line in lines:
  l = list(ast.literal_eval(line))
  tedTalk_preProcessed.append(l)

with open('C:/Users/abahr/PycharmProjects/MIR/data/persian_preProcessed.txt',encoding='utf-8') as f:
    lines = f.read().splitlines()
persian_preProcessed=[]
import ast
for line in lines:
  l = list(ast.literal_eval(line))
  persian_preProcessed.append(l)


# step 1 (preprocess):
#   input: the path to tedTalk + persian files read the files (tedTalk + persian XML)
#   output: preprocessed text in a 'documents' array or a file
#   store results in a 'documents' array or read to file


# step 2 (index construction):
#   input: the preprocessed document (path to file or an array)
#   output: positional index + bigram index (write to file)

# step 3 (index compression):
#   input: path to file containing positional index
#   output: compressed file + report statistics

# step 4 (query correction):
#   input: a query string + bigram index + positional index
#   output: corrected query :D

# step 5 (document retrieval):
#   input: a query string
#   output: list of documents :-? do you only show IDs? do you print out the documents :-? ????

