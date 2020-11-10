from ast import literal_eval


def get_word_ngrams(word, n):
    # TODO: use the nltk library instead
    ngrams = []
    for i in range(len(word)):
        left, right = max(0, i - n + 1), i + 1
        ngrams += [word[left:right]]
    return ngrams


def add_header_positional_index(text, header, docID, index, all_words):
    for posID in range(len(text)):
        word = text[posID]
        if word not in index:
            index[word] = {}
        if header not in index[word]:
            index[word][header] = {}
        if docID not in index[word][header]:
            index[word][header][docID] = [posID]
        else:
            index[word][header][docID] += [posID]
        all_words.add(word)


def add_document_tedtalk(document, docID, positional_index, bigram_index):
    all_words = set()
    description, title = document[0], document[1]
    add_header_positional_index(description, "description", docID, positional_index, all_words)
    add_header_positional_index(title, "title", docID, positional_index, all_words)
    bigram_index = get_bigram_index(all_words, bigram_index)
    return positional_index, bigram_index


def delete_document_tedtalk(document, docID, positional_index):
    description, title = document[0], document[1]
    for word in description:
        del positional_index[word]["description"][docID]


def get_positional_index_tedtalk(documents):
    tedTalk_positional_index = {}
    all_words = set()

    for docID in range(len(documents)):
        description, title = documents[docID][0], documents[docID][1]
        add_header_positional_index(description, "description", docID, tedTalk_positional_index, all_words)
        add_header_positional_index(title, "title", docID, tedTalk_positional_index, all_words)

    return tedTalk_positional_index, all_words


def get_bigram_index(all_words, bigram_index=None):
    if bigram_index is None:
        bigram_index = {}
    for word in all_words:
        word_bigrams = get_word_ngrams(word, 2)
        for bigram in word_bigrams:
            if bigram not in bigram_index:
                bigram_index[bigram] = []
            bigram_index[bigram] += [word]
    return bigram_index


def construct_index(documents):
    tedTalk_positional_index, all_words = get_positional_index_tedtalk(documents)
    bigram_index = get_bigram_index(all_words)
    return tedTalk_positional_index, bigram_index


with open('data/tokenized_tedTalk.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
documents = []
for line in lines:
    documents.append(list(literal_eval(line)))

construct_index(documents[:3])

