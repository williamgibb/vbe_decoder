# XXX Fill out docstring!
"""
test_utils.py from vbe_decoder
Created: 10/10/15

Purpose:

Examples:

Usage:

"""
# Stdlib
from __future__ import print_function
import logging
import unittest
# Third Party code
# Custom Code
import vbe_decoder.utility as utils
import vbe_decoder.constants as constants

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s [%(filename)s:%(funcName)s]')
log = logging.getLogger(__name__)


class TestDigits(unittest.TestCase):
    def setUp(self):
        self.digits = utils.make_digits()

    def test_makedigits(self):
        e = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
            24: 0,
            25: 0,
            26: 0,
            27: 0,
            28: 0,
            29: 0,
            30: 0,
            31: 0,
            32: 0,
            33: 0,
            34: 0,
            35: 0,
            36: 0,
            37: 0,
            38: 0,
            39: 0,
            40: 0,
            41: 0,
            42: 0,
            43: 62,
            44: 0,
            45: 0,
            46: 0,
            47: 63,
            48: 52,
            49: 53,
            50: 54,
            51: 55,
            52: 56,
            53: 57,
            54: 58,
            55: 59,
            56: 60,
            57: 61,
            58: 0,
            59: 0,
            60: 0,
            61: 0,
            62: 0,
            63: 0,
            64: 0,
            65: 0,
            66: 1,
            67: 2,
            68: 3,
            69: 4,
            70: 5,
            71: 6,
            72: 7,
            73: 8,
            74: 9,
            75: 10,
            76: 11,
            77: 12,
            78: 13,
            79: 14,
            80: 15,
            81: 16,
            82: 17,
            83: 18,
            84: 19,
            85: 20,
            86: 21,
            87: 22,
            88: 23,
            89: 24,
            90: 25,
            91: 0,
            92: 0,
            93: 0,
            94: 0,
            95: 0,
            96: 0,
            97: 26,
            98: 27,
            99: 28,
            100: 29,
            101: 30,
            102: 31,
            103: 32,
            104: 33,
            105: 34,
            106: 35,
            107: 36,
            108: 37,
            109: 38,
            110: 39,
            111: 40,
            112: 41,
            113: 42,
            114: 43,
            115: 44,
            116: 45,
            117: 46,
            118: 47,
            119: 48,
            120: 49,
            121: 50,
            122: 51
        }
        r = utils.make_digits()
        for k, v in e.items():
            self.assertEqual(r.get(k, 0), v)


class TestBase64(unittest.TestCase):
    def setUp(self):
        self.digits = utils.make_digits()

    def test_b64_decode1(self):
        s = 'abcdef'
        e = 2031990633
        log.info('Input: {}'.format(s))
        r = utils.decode_base64(chars=s, digits=self.digits)
        self.assertEqual(r, e)

    def test_b64_decode3(self):
        s = 'aaaaaa'
        e = 1771742825
        log.info('Input: {}'.format(s))
        r = utils.decode_base64(chars=s, digits=self.digits)
        self.assertEqual(r, e)

    def test_b64_decode2(self):
        # XXX Temporary!
        d = {'aabcde': 1977394793,
             'zzzbcd': 1910193359,
             # 'zzzzzz': 18446744072903408847,
             # '123456': 18446744073306402263,
             # '098765': 18446744073361154003,
             }
        for k, e in d.items():
            log.info('Input: {}'.format(k))
            r = utils.decode_base64(chars = k, digits=self.digits)
            self.assertEqual(r, e)


class TestLeadByte(unittest.TestCase):
    def run_list(self, cp, input_results):
        for (byte, e) in input_results:
            r = utils.is_lead_byte(codepage=cp, byte=byte)
            log.debug('codepage {} - 0x{:x} - expected {} - got {}'.format(cp, byte, e, r))
            self.assertEqual(r, e)

    def test_no_codepage(self):
        r = utils.is_lead_byte(codepage=0, byte=0x00)
        self.assertEqual(r, 0)

    def test_japan_codepage(self):
        cp = 932
        input_results = [(0x00, 0),
                         (0x79, 0),
                         (0x80, 0),
                         (0x81, 1),
                         (0x9f, 1),
                         (0xa0, 0),
                         (0xde, 0),
                         (0xdf, 0),
                         (0xe0, 1),
                         (0xfc, 1),
                         (0xfd, 0),
                         (0xff, 0)
                         ]
        self.run_list(cp=cp, input_results=input_results)

    def test_chinese_simple_codepage(self):
        cp = 936
        input_results = [(0x00, 0),
                         (0xa0, 0),
                         (0xa1, 1),
                         (0xfd, 1),
                         (0xfe, 1),
                         (0xff, 0),
                         ]
        self.run_list(cp=cp, input_results=input_results)

    def test_korean_wangsung_codepage(self):
        cp = 949
        input_results = [(0x00, 0),
                         (0x80, 0),
                         (0x81, 1),
                         (0xfd, 1),
                         (0xfe, 1),
                         (0xff, 0),
                         ]
        self.run_list(cp=cp, input_results=input_results)

    def test_chinese_big_codepage(self):
        cp = 950
        input_results = [(0x00, 0),
                         (0x80, 0),
                         (0x81, 1),
                         (0xfd, 1),
                         (0xfe, 1),
                         (0xff, 0),
                         ]
        self.run_list(cp=cp, input_results=input_results)

    def test_korean_codepage(self):
        cp = 1361
        input_results = [(0x00, 0),
                         (0x83, 0),
                         (0x84, 1),
                         (0xd3, 1),
                         (0xd4, 0),
                         (0xd8, 0),
                         (0xd9, 1),
                         (0xde, 1),
                         (0xdf, 0),
                         (0xe0, 1),
                         (0xf9, 1),
                         (0xfa, 0),
                         (0xff, 0),
                         ]
        self.run_list(cp=cp, input_results=input_results)


class TestMnemonic(unittest.TestCase):
    def test_null(self):
        r = utils.decode_mnemonic(mnemonic=None)
        self.assertEqual(r, '\x00')

    def test_duck(self):
        r = utils.decode_mnemonic(mnemonic='duck')
        self.assertEqual(r, '?')

    def test_defined_values(self):
        for k, v in constants.ENTITY_MAP.items():
            e = chr(v)
            r = utils.decode_mnemonic(mnemonic=k)
            self.assertEqual(r, e)


if __name__ == '__main__':
    unittest.main()