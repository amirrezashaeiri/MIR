from ast import literal_eval


def get_word_ngrams(word, n):
    # TODO: use the nltk library instead
    ngrams = []
    for i in range(len(word)):
        left, right = max(0, i - n + 1), i + 1
        ngrams += [word[left:right]]
    return ngrams


def construct_index(documents):
    tedTalk_title_positional_index = {}
    tedTalk_description_positional_index = {}

    # TODO: think of doing this as a function so as to remove duplicate code
    for docID in range(len(documents)):
        # description
        doc_desc = documents[docID][0]
        for posID in range(len(doc_desc)):
            word = doc_desc[posID]
            if word not in tedTalk_description_positional_index:
                tedTalk_description_positional_index[word] = {}
            if docID not in tedTalk_description_positional_index[word]:
                tedTalk_description_positional_index[word][docID] = []
            tedTalk_description_positional_index[word][docID] += [posID]

        # title
        doc_title = documents[docID][1]
        for posID in range(len(doc_title)):
            word = doc_desc[posID]
            if word not in tedTalk_title_positional_index:
                tedTalk_title_positional_index[word] = {}
            if docID not in tedTalk_title_positional_index[word]:
                tedTalk_title_positional_index[word][docID] = []
            tedTalk_title_positional_index[word][docID] += [posID]

    print(tedTalk_description_positional_index)
    print(tedTalk_title_positional_index)

    # 1. positional  index
    # traverse the elements (document) in data
    # for each document do:
    #   word = data[docID][i][ind]
    #   if i == 0: index = tedTalk_description_index
    #   else if i == 1: index = tedTalk_title_index
    #   if word not in index: index[word] = {}
    #   index[word][id] += [ind]

    bigram_index = {}

    # 2. bigram
    # traverse elements in all indexes
    # for each word in index do:
    #   word_bigrams = get_word_ngrams(2)
    #   for each bigram in word_bigram do:
    #     if bigram not in bigram_index: bigram_index[bigram] = {}
    #     bigram_index[bigram] += [word]

    return 0


with open('data/tokenized_tedTalk.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
documents = []
for line in lines:
    documents.append(list(literal_eval(line)))

construct_index(documents[:3])

