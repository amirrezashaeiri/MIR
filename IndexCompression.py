from IndexConstruction import read_index_from_file, write_index_to_file
from sys import getsizeof, byteorder
from math import ceil
import pickle


class Compressor:
    def __init__(self, index=None):
        self.positional_index = index
        self.compressed = {}
        self.decompressed = {}

    def encode_postings(self, postings):
        pass

    def compress_header(self, term, header):
        if header not in self.positional_index[term]:
            return
        self.compressed[term][header] = {}
        for docID in self.positional_index[term][header]:
            postings = self.positional_index[term][header][docID]
            self.compressed[term][header][docID] = self.encode_postings(postings)

    def decompress_header(self, term, header):
        if header not in self.compressed[term]:
            return
        self.decompressed[term][header] = {}
        for docID in self.compressed[term][header]:
            postings = self.compressed[term][header][docID]
            self.decompressed[term][header][docID] = self.decode_postings(postings)

    def compress(self):
        for term in self.positional_index:
            self.compressed[term] = {}
            self.compress_header(term, "title")
            self.compress_header(term, "text")

    def set_compressed(self, compressed):
        self.compressed = compressed

    def decompress(self):
        if self.compressed is None:
            return
        for term in self.compressed:
            self.decompressed[term] = {}
            self.decompress_header(term, "title")
            self.decompress_header(term, "text")

    def check_accuracy_header(self, term, header):
        if header not in self.positional_index[term]:
            return header not in self.decompressed[term]
        for docID in self.positional_index[term][header]:
            if docID not in self.decompressed[term][header]:
                return False
            if self.decompressed[term][header][docID] != \
                    self.positional_index[term][header][docID]:
                return False
        return True

    def check_accuracy(self):
        for term in self.positional_index:
            if not self.check_accuracy_header(term, "title"):
                print("title not accurate for " + term)
                print(self.decompressed[term]["title"])
                print(self.positional_index[term]["title"])
                return False
            if not self.check_accuracy_header(term, "text"):
                print("text not accurate for " + term)
                print(self.decompressed[term]["text"])
                print(self.positional_index[term]["text"])
                return False
        return True

    def decode_postings(self, postings):
        pass

    def encode(self, param):
        pass

    def compare(self):
        before, after = getsizeof(pickle.dumps(self.positional_index)), \
                        getsizeof(pickle.dumps(self.compressed))
        print("Before: ", before, "(B))")
        print("After Variable Bytes compression:", after, "(B)")
        print("difference:", after - before, "(B)")


class GammaCode(Compressor):
    def __init__(self, index=None):
        super().__init__(index)

    def get_offset(self, number):
        if number == 1:
            return ''
        return str(bin(number)[2:])[1:]

    def encode(self, number):
        offset = self.get_offset(number)
        unary = '1' * len(offset)
        g = unary + '0' + offset
        return int(g, 2).to_bytes(ceil(len(g) / 8), byteorder)

    def decode_postings(self, postings):
        reading_unary, reading_offset = True, False
        ids = []
        length, number, power_of_two = 0, 0, 0
        postings = str(format(int.from_bytes(postings, byteorder), 'b'))
        for b in postings:
            if reading_unary:
                if b:
                    length += 1
                else:
                    if length == 0:
                        ids += [1]
                    else:
                        reading_unary, reading_offset = False, True
                        power_of_two = 2 ** length
            elif reading_offset:
                number *= 2
                number += b
                length -= 1
                if length <= 0:
                    ids += [number + power_of_two]
                    number, power_of_two = 0, 0
                    reading_unary, reading_offset = True, False

        if power_of_two > 0:
            ids += [power_of_two]
        for i in range(1, len(ids)):
            ids[i] += ids[i - 1]
        return ids

    def encode_postings(self, postings):
        g = []
        prev_posID = 0
        for posID in postings:
            g += self.encode(posID - prev_posID)
            prev_posID = posID
        return g


class VariableByteCode(Compressor):

    def __init__(self, index=None):
        super().__init__(index)

    def encode(self, number):
        vb = []
        while True:
            vb = [number % 128] + vb
            if number < 128:
                break
            number //= 128
        vb[-1] += 128
        return bytearray(vb)

    def encode_postings(self, postings):
        g = []
        prev_posID = 0
        for posID in postings:
            g += self.encode(posID - prev_posID)
            prev_posID = posID
        return g

    def decode_postings(self, postings):
        ids, curr_gap = [], 0
        for b in bytearray(postings):
            curr_gap *= 128
            if b < 128:
                curr_gap += int(b)
            else:
                curr_gap += (int(b) - 128)
                ids += [curr_gap]
                curr_gap = 0
        for i in range(1, len(ids)):
            ids[i] += ids[i - 1]
        return ids


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
