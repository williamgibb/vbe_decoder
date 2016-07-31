# XXX Fill out docstring!
"""
test_decoder.py from vbe_decoder
Created: 07/30/16

Purpose:

Examples:

Usage:

"""
# Stdlib
from __future__ import print_function
import logging
import os
import unittest
# Third Party code
# Custom Code
import vbe_decoder

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s [%(filename)s:%(funcName)s]')
log = logging.getLogger(__name__)


ASSETS_PATH = os.path.join(os.path.split(__file__)[0], 'assets')


class TestDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = vbe_decoder.decoder.Decoder()

    def run_decoder(self, input_buf_fp, expected_buf_fp):
        with open(input_buf_fp, 'rb') as f:
            inbuf = f.read()
        with open(expected_buf_fp, 'rb') as f:
            outbuf = f.read()
        self.decoder.decode(inbuf)
        decoded_buf = self.decoder.output_buf
        self.assertEqual(outbuf, decoded_buf)

    def test_contrato(self):
        log.info('Running contrato test')
        infp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware')
        opfp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware.decoded')
        self.run_decoder(input_buf_fp=infp, expected_buf_fp=opfp)