from __future__ import unicode_literals

import re

from hazm import *
import ast

def prepare_text_persian(pages_data):
    ##### tokenize, normalization, delete punct######

    tokenized_pages=[]
    for page in pages_data:
        tokenized_page = ""
        for letter in page:
            m = re.search('^[آ-ی]$', letter)
            if (m is None):
                tokenized_page += " "
            else:
                tokenized_page += letter
        tokenized_pages.append(tokenized_page)

    #######lemmatize, stemming######




    # stemmer = Stemmer()
    # tokenized_stemmed_pages=[]
    # for tokenized_page in tokenized_pages :
    #   tokenized_stemmed_page=[]
    #   for word in tokenized_page.split():
    #     tokenized_stemmed_page.append(stemmer.stem(word))
    #   tokenized_stemmed_pages.append(tokenized_stemmed_page)

    lemmatizer = Lemmatizer()
    tokenized_lemmatized_pages = []
    for tokenized_page in tokenized_pages:
        tokenized_lemmatized_page = []
        for word in tokenized_page.split():
            if (len(lemmatizer.lemmatize(word).split("#")) == 1):
                tokenized_lemmatized_page.append(lemmatizer.lemmatize(word).split("#")[0])
            else:
                tokenized_lemmatized_page.append(lemmatizer.lemmatize(word).split("#")[1])
        tokenized_lemmatized_pages.append(tokenized_lemmatized_page)

    return tokenized_lemmatized_pages


def remove_stopwords_persian(tokenized_lemmatized_pages):
    ########remove stopwords##########

    # def remove_stop_words(tokenized_lemmatized):

    list_of_words_frequency = []
    for tokenized_lemmatized_page in tokenized_lemmatized_pages:
        for word in tokenized_lemmatized_page:

            flag = 0
            for i in range(len(list_of_words_frequency)):
                if (list_of_words_frequency[i][0] == word):
                    flag = 1
                    list_of_words_frequency[i][1] += 1
                if (i > 2000):
                    flag = 1
                    break
            if (flag == 0):
                list_of_words_frequency.append([word, 1])

    list_of_words_frequency = sorted(list_of_words_frequency, key=lambda l: l[1], reverse=True)

    number_of_stop_words = 13

    stop_words = [i[0] for i in list_of_words_frequency][:number_of_stop_words]
    with open('C:/Users/abahr/PycharmProjects/MIR/data/stop_words_persian.txt', 'w', encoding='utf-8') as f:
        for page in stop_words:
            f.write("%s\n" % page)


    tokenized_lemmatized_removed_stop_words_pages = []
    for tokenized_lemmatized_page in tokenized_lemmatized_pages:

        tokenized_lemmatized_removed_stop_words_page = [word for word in tokenized_lemmatized_page if word not in stop_words]
        tokenized_lemmatized_removed_stop_words_pages.append(tokenized_lemmatized_removed_stop_words_page)
    return tokenized_lemmatized_removed_stop_words_pages

def remove_stopwords_title_persian(title_tokenized_lemmatized_pages):

    with open('C:/Users/abahr/PycharmProjects/MIR/data/stop_words_persian.txt', encoding='utf-8') as f:
        lines = f.read().splitlines()
    stop_words = lines

    tokenized_lemmatized_removed_stop_words_title = [word for word in title_tokenized_lemmatized_pages if
                                                    word not in stop_words]
    return tokenized_lemmatized_removed_stop_words_title

def merge_text_title_and_add_id_persian(title_tokenized_lemmatized_removed_stop_words_pages,text_tokenized_lemmatized_removed_stop_words_pages):
    merged_id_text_title = []

    for i in range(len(title_tokenized_lemmatized_removed_stop_words_pages)):
        merged_id_text_title.append([i+1, text_tokenized_lemmatized_removed_stop_words_pages[i],
                                     title_tokenized_lemmatized_removed_stop_words_pages[i]])
    return merged_id_text_title

def string_preProcess_persian(str):
    tokenized_str = ""
    for letter in str:
        m = re.search('^[آ-ی]$', letter)
        if (m is None):
            tokenized_str += " "
        else:
            tokenized_str += letter
    lemmatizer = Lemmatizer()

    tokenized_lemmatized_str = []
    for word in tokenized_str.split():
        if (len(lemmatizer.lemmatize(word).split("#")) == 1):
            tokenized_lemmatized_str.append(lemmatizer.lemmatize(word).split("#")[0])
        else:
            tokenized_lemmatized_str.append(lemmatizer.lemmatize(word).split("#")[1])
    with open('C:/Users/abahr/PycharmProjects/MIR/data/stop_words_persian.txt', encoding='utf-8') as f:
        lines = f.read().splitlines()
    stop_words = lines
    import ast

    tokenized_lemmatized_removed_stop_words_str = [word for word in tokenized_lemmatized_str if
                                                    word not in stop_words]
    return tokenized_lemmatized_removed_stop_words_str



# parse an xml file by name
# #text
# mydoc = minidom.parse('C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/Persian.xml')
# items_text = mydoc.getElementsByTagName('text')
#
# pages_text_data=[items_text[i].firstChild.data for i in range (len(items_text))]
#
# text_tokenized_lemmatized_pages= prepare_text(pages_text_data)
# text_tokenized_lemmatized_removed_stop_words_pages=remove_stopwords(text_tokenized_lemmatized_pages)
#
# #title
# items_title = mydoc.getElementsByTagName('title')
#
# pages_title_data=[items_title[i].firstChild.data for i in range (len(items_title))]
#
# title_tokenized_lemmatized_pages= prepare_text(pages_title_data)
# title_tokenized_lemmatized_removed_stop_words_pages=remove_stopwords(title_tokenized_lemmatized_pages)
#
#
# merged_id_text_title=merge_text_title_and_add_id(title_tokenized_lemmatized_removed_stop_words_pages,text_tokenized_lemmatized_removed_stop_words_pages)

#
# with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_persian.txt', 'w',encoding='utf-8') as f:
#     for page in merged_id_text_title:
#         f.write("%s\n" % page)

# with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_persian.txt',encoding='utf-8') as f:
#     lines = f.read().splitlines()
# persian_preProcessed=[]
# import ast
# for line in lines:
#   l = list(ast.literal_eval(line))
#   persian_preProcessed.append(l)
#
