from ast import literal_eval
# TODO: think about docID
# TODO: think about deleting documents and how to update bigram


def get_word_ngrams(word, n):
    ngrams = []
    for i in range(len(word)):
        left, right = max(0, i - n + 1), i + 1
        ngrams += [word[left:right]]
    return ngrams


def add_document(document, docID, positional_index, bigram_index):
    add_header_positional_index(document[0], "text", docID, positional_index)
    add_header_positional_index(document[1], "title", docID, positional_index)
    bigram_index = get_bigram_index(set(document[0]), bigram_index)
    bigram_index = get_bigram_index(set(document[1]), bigram_index)
    return positional_index, bigram_index


def delete_document(document, docID, positional_index):
    for word in document[0]:
        del positional_index[word]["text"][docID]

    for word in document[1]:
        del positional_index[word]["title"][docID]


def add_header_positional_index(words, header, docID, index):
    for posID in range(len(words)):
        word = words[posID]
        if word not in index:
            index[word] = {}
        if header not in index[word]:
            index[word][header] = {}
        if docID not in index[word][header]:
            index[word][header][docID] = [posID]
        else:
            index[word][header][docID] += [posID]


def get_positional_index(documents):
    positional_index = {}
    for docID in range(len(documents)):
        add_header_positional_index(documents[docID][0], "text", docID, positional_index)
        add_header_positional_index(documents[docID][1], "title", docID, positional_index)
    return positional_index


def get_bigram_index(words, index=None):
    if index is None:
        index = {}
    for word in words:
        bigrams = get_word_ngrams(word, 2)
        for bigram in bigrams:
            if bigram not in index:
                index[bigram] = [word]
            else:
                index[bigram] += [word]
    return index


def construct_index(documents):
    positional_index = get_positional_index(documents)
    bigram_index = get_bigram_index(positional_index.keys())
    return positional_index, bigram_index


with open('data/tokenized_tedTalk.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
documents = []
for line in lines:
    documents.append(list(literal_eval(line)))

construct_index(documents[:3])

