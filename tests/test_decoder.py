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
            inbuf = f.read().decode()
        with open(expected_buf_fp, 'rb') as f:
            outbuf = f.read().decode()
        self.decoder.decode(inbuf)
        decoded_buf = self.decoder.output_buf
        self.assertEqual(outbuf, decoded_buf)

    def test_bytearray_input(self):
        log.info('Running contrato test w/ bytearray input')
        infp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware')
        opfp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware.decoded')
        with open(infp, 'rb') as f:
            inbuf = f.read()
        with open(opfp, 'rb') as f:
            outbuf = f.read().decode()
        self.assertIsInstance(inbuf, bytes)
        self.decoder.decode(inbuf)
        decoded_buf = self.decoder.output_buf
        self.assertEqual(outbuf, decoded_buf)

    def test_contrato(self):
        log.info('Running contrato test')
        infp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware')
        opfp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware.decoded')
        self.run_decoder(input_buf_fp=infp, expected_buf_fp=opfp)

    def test_houdini(self):
        log.info('Running houdini test')
        infp = os.path.join(ASSETS_PATH, 'GLsRBXbT.vbe.malware')
        opfp = os.path.join(ASSETS_PATH, 'GLsRBXbT.vbe.malware.decoded')
        self.run_decoder(input_buf_fp=infp, expected_buf_fp=opfp)

    def test_class_resuse(self):
        log.info('Running contrato test with class reuse / reset()')
        infp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware')
        opfp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware.decoded')
        self.run_decoder(input_buf_fp=infp, expected_buf_fp=opfp)
        obuf1 = self.decoder.output_buf
        self.decoder.reset()
        self.run_decoder(input_buf_fp=infp, expected_buf_fp=opfp)
        self.assertEqual(self.decoder.output_buf, obuf1)

    def test_bad_input(self):
        log.info('Running test with bad input')
        with self.assertRaises(vbe_decoder.DecodeError):
            self.decoder.decode(buf=1234)

    def test_more_bad_input(self):
        log.info('Running test with more bad input')
        with self.assertRaises(vbe_decoder.DecodeError):
            self.decoder.decode(buf={'foo':'bar'})

    def test_dumb_decoder(self):
        self.decoder = vbe_decoder.Decoder(dumb=True)
        log.info('Running contrato test with dumb option')
        infp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware')
        opfp = os.path.join(ASSETS_PATH, 'contrato.vbe.malware.decoded')
        self.run_decoder(input_buf_fp=infp, expected_buf_fp=opfp)

    def test_bad_creation_options(self):
        with self.assertRaises(vbe_decoder.DecodeError):
            vbe_decoder.Decoder(url_encoded=True,
                                html_encoded=True)