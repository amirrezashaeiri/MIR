from ast import literal_eval
import pickle
# TODO: think about docID
# TODO: think about deleting documents and how to update bigram


def get_word_ngrams(word, n):
    ngrams = []
    for i in range(len(word)):
        left, right = max(0, i - n + 1), i + 1
        ngrams += [word[left:right]]
    return ngrams


def write_index_to_file(index, name):
    file = open(name, 'wb')
    pickle.dump(index, file)
    file.close()


def read_index_from_file(name):
    file = open(name, 'rb')
    index = pickle.load(file)
    file.close()
    return index


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
    for document in documents:
        add_header_positional_index(document[1], "text", document[0], positional_index)
        add_header_positional_index(document[2], "title", document[0], positional_index)
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


tedTalks = open('data/tokenized_tedTalk_with_id.txt', encoding='utf-8')
tedTalks_documents = []
for line in tedTalks.read().splitlines():
    tedTalks_documents.append(list(literal_eval(line)))

pos_index_tedtalks, bigram_index_tedtalks = construct_index(tedTalks_documents)
write_index_to_file(pos_index_tedtalks, "positional_index_tedTalks.pkl")
write_index_to_file(bigram_index_tedtalks, "bigram_index_tedTalks.pkl")

persian = open('data/tokenized_persian_with_id.txt', encoding='utf-8')
persian_documents = []
for line in persian.read().splitlines():
    persian_documents.append(list(literal_eval(line)))

pos_index_persian, bigram_index_persian = construct_index(persian_documents)
write_index_to_file(pos_index_persian, "positional_index_persian.pkl")
write_index_to_file(bigram_index_persian, "bigram_index_persian.pkl")
