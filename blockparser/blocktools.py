import struct
import hashlib


def uint1(stream):
    return ord(stream.read(1))


def uint2(stream):
    return struct.unpack('H', stream.read(2))[0]


def uint4(stream):
    # type: (object) -> object
    return struct.unpack('I', stream.read(4))[0]


def uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]


def hash32(stream):
    return stream.read(32)[::-1]


def time(stream):
    time = uint4(stream)
    return time


def varint(stream):
    size = uint1(stream)

    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint2(stream)
    if size == 0xfe:
        return uint4(stream)
    if size == 0xff:
        return uint8(stream)
    return -1


def hashStr(bytebuffer):
    # return binascii.hexlify(pk_script)
    return ''.join(('%02x' % ord(a)) for a in bytebuffer)

# modification by Peng

def double_sha256(bytebuffer):
    return hashlib.sha256(hashlib.sha256(bytebuffer).digest()).digest()


def byte2int(bytebuffer):
    hash_obj = hashlib.sha256(bytebuffer)
    hex_dig = hash_obj.hexdigest()
    # print int(hex_dig)
    return int(hex_dig, 16) % 2147483647


def hash2int(hash_hex):
    return int(hash_hex, 16) % 2147483647


def rawpk2hash160(pk_script):
    return pk_script[pk_script.find('\x14')+1:]


def rawpk2addr(pk_script):
    import base58
    return base58.hash_160_to_bc_address(rawpk2hash160(pk_script))

