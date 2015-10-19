"""
__main__.py.py from vbe_decoder
Created: 10/18/15

Purpose:  Convenience wrapper for vbe_decoder class.

Usage:
python -m vbe_decoder -i <file to decode> -o <file to write too> <options>
"""
# Stdlib
from __future__ import print_function
import argparse
import logging
import sys
# Custom Code
import vbe_decoder

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s [%(filename)s:%(funcName)s]')
log = logging.getLogger(__name__)

__author__ = 'wgibb'


def main(options):
    if not options.verbose:
        logging.disable(logging.DEBUG)
    d = vbe_decoder.Decoder(dumb=options.dumb,
                            codepage=options.codepage,
                            url_encoded=options.urldec,
                            html_encoded=options.htmldec)
    with open(options.input, 'rb') as f:
        buf = f.read()
    d.decode(buf=buf)
    with open(options.output, 'wb') as f:
        f.write(d.output_buf)
    sys.exit(0)


def makeargpaser():
    epilog = '''Code pages can be the following:
932 - Japanese, 936 - Chinese (Simplified), 950 - Chinese (Traditional), 949 - Korean (Wansung), 1361 - Korean (Johab).
Any other code pages don't need to be specified.'''
    parser = argparse.ArgumentParser(description="Decode an encoded VB Script.", epilog=epilog)
    parser.add_argument('-i', '--input', dest='input', required=True, action='store',
                        help='Input file.')
    parser.add_argument('-o', '--output', dest='output', required=True, action='store',
                        help='Output file.')
    parser.add_argument('-c', '--codepage', dest='codepage', default=0, action='store', type=int,
                        help='Specify a codepage.')
    parser.add_argument('-d', '--dumb', dest='dumb', default=False, action='store_true',
                        help='Use this switch if you do not want to use the HTMLGuadian defeation mechanism')
    mux = parser.add_mutually_exclusive_group(required=False)
    mux.add_argument('--urldec', dest='urldec', default=False, action='store_true',
                     help='Use to unescape %%xx style encoding on the fly')
    mux.add_argument('--htmldec', dest='htmldec', default=False, action='store_true',
                     help='Use to unescape & style encoding on the fly')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true',
                        help='Enable verbose output')
    return parser


if __name__ == '__main__':
    p = makeargpaser()
    opts = p.parse_args()
    main(opts)
