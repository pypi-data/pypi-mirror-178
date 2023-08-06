from sys import getdefaultencoding

SYS_ENCODING = getdefaultencoding()

def decode(b: bytes) -> str:
    return b.decode(SYS_ENCODING)
