"""Dummy module so we can build docs and use auto-completion using standard
python.
"""

LITTLE_ENDIAN = 0
BIG_ENDIAN = 1
NATIVE = 2

PTR = 0x02000000
ARRAY = 0xc000000

UINT8 = 0x00000000
UINT16 = 0x10000000
UINT32 = 0x20000000
UINT64 = 0x30000000
INT8 = 0x08000000
INT16 = 0x18000000
INT32 = 0x28000000
INT64 = 0x38000000
FLOAT32 = 0xf0000000
FLOAT32 = 0xf8000000


def sizeof(struct):
    return 0


def addressof(obj):
    return 0


def bytes_at(addr, size):
    return bytes(size)


def bytearray_at(addr, size):
    return bytearray(size)


class struct():
    def __init__(self, addr, descriptor, layout_type=NATIVE):
        pass
