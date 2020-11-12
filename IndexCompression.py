from struct import pack, unpack
from math import log
from IndexConstruction import read_index_from_file, write_index_to_file
# TODO: think about how to infer zero :-?


def vb_encode_number(number):
    vb = []
    while True:
        vb += [number % 128]
        if number < 128:
            break
        number //= 128
    vb[0] += 128
    vb.reverse()
    return pack('%dB' % len(vb), *vb)


def vb_encode(numbers):
    vb = []
    prev_number = 0
    for number in numbers:
        vb += [vb_encode_number(number - prev_number)]
        prev_number = number
    return b"".join(vb)


# TODO: change to cumsum
def vb_decode(vb):
    vb = unpack('%dB' % len(vb), vb)
    curr, decoded = 0, []
    for byte in vb:
        curr *= 128
        if byte < 128:
            curr += byte
        else:
            curr += (byte - 128)
            decoded += [curr]
            curr = 0
    return decoded


# TODO: special case for zero
def gamma_encoding_get_offset(number):
    length = int(log(number, 2))
    return length, number - 2 ** length


def gamma_encoding_get_unary(number):
    return 2 ** int(log(number, 2)) - 1


def gamma_encode_number(number):
    unary = gamma_encoding_get_unary(number)
    length, offset = gamma_encoding_get_offset(number)
    return (unary << (length + 1)) + offset


def gamma_encode(numbers):
    gamma = ''
    for number in numbers:
        gamma += bin(gamma_encode_number(number))
    return gamma


def vb_encode_index(index):
    for word in index.keys():
        if "title" in index[word]:
            for docID in index[word]["title"]:
                postings = index[word]["title"][docID]
                index[word]["title"][docID] = vb_encode(postings)
        if "text" in index[word]:
            for docID in index[word]["text"]:
                postings = index[word]["text"][docID]
                index[word]["text"][docID] = vb_encode(postings)
