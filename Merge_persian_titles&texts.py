#######merge title and text of persian#########
# import ast
# with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_titles_persian.txt',encoding='utf-8') as f:
#     lines = f.read().splitlines()
# tokenized_lemmatized_removed_stop_words_persian_titles=[]
#
# for line in lines:
#   l = list(ast.literal_eval(line))
#   tokenized_lemmatized_removed_stop_words_persian_titles.append(l)
#
# with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_persian.txt',encoding='utf-8') as f:
#     lines = f.read().splitlines()
# tokenized_lemmatized_removed_stop_words_persian_text=[]
#
# for line in lines:
#   l = list(ast.literal_eval(line))
#   tokenized_lemmatized_removed_stop_words_persian_text.append(l)
#
# merged_text_title =[]
#
# for i in range(len(tokenized_lemmatized_removed_stop_words_persian_titles)):
#     merged_text_title.append([tokenized_lemmatized_removed_stop_words_persian_text[i],tokenized_lemmatized_removed_stop_words_persian_titles[i]])
# with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_textTitles_persian.txt', 'w',encoding='utf-8') as f:
#     for page in merged_text_title:
#         f.write("%s\n" % page)


####add id to English prerpcess#######
#
# with open('C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/tokenized_tedTalk.txt',encoding='utf-8') as f:
#     lines = f.read().splitlines()
# tokenized_lemmatized_removed_stop_words_tedTalk_desc_title=[]
# import ast
# for line in lines:
#   l = list(ast.literal_eval(line))
#   tokenized_lemmatized_removed_stop_words_tedTalk_desc_title.append(l)
#
# merged_id_english =[]
#
# for i in range(len(tokenized_lemmatized_removed_stop_words_tedTalk_desc_title)):
#     merged_id_english.append([i,tokenized_lemmatized_removed_stop_words_tedTalk_desc_title[i][0],tokenized_lemmatized_removed_stop_words_tedTalk_desc_title[i][1]])
# with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_tedTalk_with_id.txt', 'w',encoding='utf-8') as f:
#     for page in merged_id_english:
#         f.write("%s\n" % page)
#

####add id to Persian prerpcess#######

with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_textTitles_persian.txt',encoding='utf-8') as f:
    lines = f.read().splitlines()
tokenized_lemmatized_removed_stop_words_persian_titles=[]
import ast
for line in lines:
  l = list(ast.literal_eval(line))
  tokenized_lemmatized_removed_stop_words_persian_titles.append(l)

merged_id_persian =[]

for i in range(len(tokenized_lemmatized_removed_stop_words_persian_titles)):
    merged_id_persian.append([i,tokenized_lemmatized_removed_stop_words_persian_titles[i][0],tokenized_lemmatized_removed_stop_words_persian_titles[i][1]])
with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_persian_with_id.txt', 'w',encoding='utf-8') as f:
    for page in merged_id_persian:
        f.write("%s\n" % page)

