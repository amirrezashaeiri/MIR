import ast
with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_titles_persian.txt',encoding='utf-8') as f:
    lines = f.read().splitlines()
tokenized_lemmatized_removed_stop_words_persian_titles=[]

for line in lines:
  l = list(ast.literal_eval(line))
  tokenized_lemmatized_removed_stop_words_persian_titles.append(l)

with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_persian.txt',encoding='utf-8') as f:
    lines = f.read().splitlines()
tokenized_lemmatized_removed_stop_words_persian_text=[]

for line in lines:
  l = list(ast.literal_eval(line))
  tokenized_lemmatized_removed_stop_words_persian_text.append(l)

merged_text_title =[]

for i in range(len(tokenized_lemmatized_removed_stop_words_persian_titles)):
    merged_text_title.append([tokenized_lemmatized_removed_stop_words_persian_text[i],tokenized_lemmatized_removed_stop_words_persian_titles[i]])
with open('C:/Users/abahr/PycharmProjects/MIR/data/tokenized_textTitles_persian.txt', 'w',encoding='utf-8') as f:
    for page in merged_text_title:
        f.write("%s\n" % page)
