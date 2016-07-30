"""
utility.py from vbe_decoder
Created: 10/18/15

Purpose: Utility functions used by vbe_decoder
"""
# Stdlib
from __future__ import print_function
import logging
# Custom Code
from vbe_decoder import exc
from vbe_decoder import constants as c

log = logging.getLogger(__name__)


def make_digits():
    digits = {0x2b: 62,
              0x2f: 63}
    for i in range(0, 26):
        digits[65 + i] = i
        digits[97 + i] = i + 26
    for i in range(0, 10):
        digits[48 + i] = 52 + i
    return digits


def decode_mnemonic(mnemonic):
    ret = c.ENTITY_MAP.get(mnemonic)
    if ret is None:
        return "?"
    return chr(ret)


def unescape(char):
    escape_map = {'#': '\r',
                  '&': '\n',
                  '!': '<',
                  '*': '>',
                  '$': '@'}
    if ord(char) > 127:
        return char
    for escape, escaped in escape_map.items():
        if escape == char:
            return escaped
    return '?'


def decode_base64(chars, digits):
    if len(chars) != 6:
        raise exc.InternalError('Decode does not have the correct number of bytes')
    ret = 0
    for i, char in enumerate(chars):
        lookup_value = ord(char)
        v = digits.get(lookup_value)
        # log.debug("{}: {:x}".format(i, v))
        if i == 0:
            d = v << 2
            # log.debug("0x{:x}".format(d))
            ret += d
        if i == 1:
            d = v >> 4
            # log.debug("0x{:x}".format(d))
            ret += d
            d = (v & 0xf) << 12
            # log.debug("0x{:x}".format(d))
            ret += d
        if i == 2:
            d = (v >> 2) << 8
            # log.debug("0x{:x}".format(d))
            ret += d
            d = (v & 0x3) << 22
            # log.debug("0x{:x}".format(d))
            ret += d
        if i == 3:
            d = v << 16
            # log.debug("0x{:x}".format(d))
            ret += d
        if i == 4:
            d = (v << 2) << 24
            # log.debug("0x{:x}".format(d))
            ret += d
        if i == 5:
            d = (v >> 4) << 24
            # log.debug("0x{:x}".format(d))
            ret += d
            # log.debug('val: {:x}'.format(ret))
    return ret


def is_lead_byte(codepage, byte):
    """

    Code page   932 - Japanese Shift-JIS        0x81-0x9f
                                                0xe0-0xfc
                936 - Simplified Chinese GBK    0xa1-0xfe
                949 - Korean Wansung            0x81-0xfe
                950 - Traditional Chinese Big5  0x81-0xfe
                1361 - Korean Johab             0x84-0xd3
                                                0xd9-0xde
                                                0xe0-0xf9

    :param codepage:
    :param byte:
    :return:
    """

    ret = 0
    if codepage == 932:
        if 0x80 < byte < 0xa0:
            ret = 1
        elif 0xdf < byte < 0xfd:
            ret = 1
    if codepage == 936:
        if 0xa0 < byte < 0xff:
            ret = 1
    if codepage in [949, 950]:
        if 0x80 < byte < 0xff:
            ret = 1
    if codepage == 13961:
        if 0x83 < byte < 0xd4:
            ret = 1
        elif 0xd8 < byte < 0xdf:
            ret = 1
        elif 0xdf < byte < 0xfa:
            ret = 1
    return ret


def make_trans():
    ret = [{} for i in range(3)]
    for i in range(32):
        for j in range(3):
            ret[j][i] = i
    for i in range(31, 128):
        for j in range(3):
            indx = (i - 31) * 3 + j
            # log.info("{}, {}, {}".format(i, j, indx))
            rdi = c.RAW_DATA[indx]
            v = i
            if i == 31:
                v = 9
            ret[j][rdi] = v
    return ret
