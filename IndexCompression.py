from struct import pack, unpack


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
    for number in numbers:
        vb += [vb_encode_number(number)]
    return b"".join(vb)


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
