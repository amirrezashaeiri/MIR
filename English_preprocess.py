import pandas as pd
data = pd.read_csv("C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/ted_talks.csv")
def prepare_text(data):
    data_desc_title=data[['description','title']]
    data_desc_title_ls=data_desc_title.values.tolist()

    ##### tokenization, casefolding#####
    import nltk
    nltk.download('punkt')

    from nltk.tokenize import word_tokenize
    tokenized=[]
    for data in data_desc_title_ls:
      tokenized_desc=word_tokenize(data[0].lower())
      tokenized_title=word_tokenize(data[1].lower())
      tokenized.append([tokenized_desc, tokenized_title])

    ###### normalization, lemmatization,and removing punctuation marks########
    import nltk
    nltk.download('wordnet')
    import nltk
    nltk.download('averaged_perceptron_tagger')
    nltk.download("punkt")

    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    from nltk.corpus import wordnet


    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)


    lemmatizer = WordNetLemmatizer()

    tokenized_lemmatized = []
    for data in tokenized:
        lemmatized_tokenized_desc = []
        for word in data[0]:
            lemmatized_tokenized_desc.append(lemmatizer.lemmatize(word, get_wordnet_pos(word)))

        lemmatized_tokenized_desc = [word for word in lemmatized_tokenized_desc if word.isalnum()]

        lemmatized_tokenized_title = []
        for word in data[1]:
            lemmatized_tokenized_title.append(lemmatizer.lemmatize(word, get_wordnet_pos(word)))

        lemmatized_tokenized_title = [word for word in lemmatized_tokenized_title if word.isalnum()]

        tokenized_lemmatized.append([lemmatized_tokenized_desc, lemmatized_tokenized_title])
    return tokenized_lemmatized
def remove_stop_words(tokenized_lemmatized):
    ######stop words#######
    list_of_words_frequency = []
    for data in tokenized_lemmatized:
        for word in data[0]:
            if (word not in [i[0] for i in list_of_words_frequency]):
                list_of_words_frequency.append([word, 1])
            else:
                list_of_words_frequency[[i[0] for i in list_of_words_frequency].index(word)][1] += 1
        for word in data[1]:
            if (word not in [i[0] for i in list_of_words_frequency]):
                list_of_words_frequency.append([word, 1])
            else:
                list_of_words_frequency[[i[0] for i in list_of_words_frequency].index(word)][1] += 1

    list_of_words_frequency=sorted(list_of_words_frequency,key=lambda l:l[1], reverse=True)

    number_of_stop_words = 10
    stop_words = [i[0] for i in list_of_words_frequency][:number_of_stop_words]
    tokenized_lemmatized_removed_stop_words = []
    for data in tokenized_lemmatized:
        lemmatized_tokenized_removed_stop_words_desc = [word for word in data[0] if word not in stop_words]

        lemmatized_tokenized_removed_stop_words_title = [word for word in data[1] if word not in stop_words]

        tokenized_lemmatized_removed_stop_words.append(
            [lemmatized_tokenized_removed_stop_words_desc, lemmatized_tokenized_removed_stop_words_title])
    return tokenized_lemmatized_removed_stop_words
tokenized_lemmatized=prepare_text(data)
tokenized_lemmatized_removed_stop_words=remove_stop_words(tokenized_lemmatized)
with open('C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/tokenized_tedTalk.txt', 'w',encoding='utf-8') as f:
    for item in tokenized_lemmatized_removed_stop_words:
        f.write("%s\n" % item)

with open('C:/Users/abahr/PycharmProjects/MIRproj/project_phase1/data/tokenized_tedTalk.txt',encoding='utf-8') as f:
    lines = f.read().splitlines()
tokenized_lemmatized_removed_stop_words_tedTalk_desc_title=[]
import ast
for line in lines:
  l = list(ast.literal_eval(line))
  tokenized_lemmatized_removed_stop_words_tedTalk_desc_title.append(l)




