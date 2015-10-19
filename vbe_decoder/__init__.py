"""
__init__.py from vbe_decoder
Created: 10/10/15

Purpose: Python port of srcdec.c for decoding encoded visual basic files.

Examples:

Usage:

License/Copyright:

From https://gist.github.com/bcse/1834878
/**********************************************************************/
/* scrdec.c - Decoder for Microsoft Script Encoder                    */
/* Version 1.8                                                        */
/*                                                                    */
/* COPYRIGHT:                                                         */
/* (c)2000-2005 MrBrownstone, mrbrownstone@ virtualconspiracy.com     */
/* v1.8 Now correctly decodes characters 0x00-0x1F, thanks to 'Zed'   */
/* v1.7 Bypassed new HTMLGuardian protection and added -dumb switch   */
/*       to disable this                                              */
/* v1.6 Added HTML Decode option (-htmldec)                           */
/* v1.5 Bypassed a cleaver trick defeating this tool                  */
/* v1.4 Some changes by Joe Steele to correct minor stuff             */
/*                                                                    */
/* DISCLAIMER:                                                        */
/* This program is for demonstrative and educational purposes only.   */
/* Use of this program is at your own risk. The author cannot be held */
/* responsible if any laws are broken by use of this program.         */
/*                                                                    */
/* If you use or distribute this code, this message should be held    */
/* intact. Also, any program based upon this code should display the  */
/* copyright message and the disclaimer.                              */
/**********************************************************************/

From http://web.archive.org/web/20141014044619/http://www.virtualconspiracy.com/content/scrdec/legal

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
# Stdlib
from __future__ import print_function
import logging
# Third Party code
# Custom Code
from . import constants as c
from . import utility
from . import exc
log = logging.getLogger(__name__)
__author__ = 'wgibb'
__version__ = '0.0.1'




class Decoder(object):
    def __init__(self, dumb=False, codepage=0, url_encoded=False, html_encoded=False):
        # Required actions
        self.digits = utility.make_digits()
        self.transform_map = utility.make_trans()
        # Build a state to function call map
        self.state_to_func = {}
        for v in dir(c):
            if not v.startswith('STATE_'):
                continue
            k = getattr(c, v)
            f = getattr(self, v.lower())
            if not f:
                raise exc.DecodeError('Unable to find function for {}'.format(v))
            self.state_to_func[k] = f

        # Items set during construction
        self.smart = 1
        self.codepage = 0
        self.url_encoded = 0
        self.html_encoded = 0

        if dumb:
            self.smart = 0
        if codepage not in c.VALID_CODEPAGES:
            raise exc.DecodeError('Invalid codepage provided: {}'.format(codepage))
        self.codepage = codepage
        if url_encoded:
            self.url_encoded = 1
        if html_encoded:
            self.html_encoded = 1
        if self.url_encoded and self.html_encoded:
            # XXX This constraint is not enforced by the c code.
            raise exc.DecodeError('Cannot do url and html decodeding together')

        # Variables which may be modified during each run.
        # State values
        self.state = c.STATE_INIT_COPY
        self.ustate = 0
        self.nextstate = 0

        # Input / output buffers
        self.buf = ''
        self.output_buf = ''
        # Temporary buffers for storing data in processing
        self.in_buf = ''
        self.out_buf = ''
        self.len_buf = ''
        self.csbuf = ''
        self.htmldec = ''

        # Holders for urlencodeding / htmldecoder
        self.c1 = 0
        self.c2 = 0

        # Integers / ptrs we need.
        self.buf_ptr = 0
        self.i = 0
        self.j = 0
        # Assorted flags
        self.csum = 0
        self.ml = 0
        self.m = 0
        self.k = 0
        self.hd = 0
        self.utf8 = 0
        self.len = 0

    def __repr__(self):
        s = '<Decoder @ {},'.format(hex(id(self)))
        s += 'i: {}, j:{},  len: {}, buf_ptr: {}, state: {},'.format(self.i, self.j, self.len, self.buf_ptr, self.state)
        s += 'smart: {}, url_encoded: {}, html_encoded: {}'.format(self.smart, self.url_encoded, self.html_encoded)
        s += '>'
        return s

    def reset(self):
        """
        Resets internal states to their initial conditions.
        This is automatically called prior to executing the 'decode' routine.

        :return:
        """
        log.debug('Reseting decoder.')
        # State values
        self.state = c.STATE_INIT_COPY
        self.ustate = 0
        self.nextstate = 0

        # Input / output buffers
        self.buf = ''
        self.output_buf = ''
        # Temporary buffers for storing data in processing
        self.in_buf = ''
        self.out_buf = ''
        self.len_buf = ''
        self.csbuf = ''
        self.htmldec = ''

        # Holders for urlencodeding / htmldecoder
        self.c1 = 0
        self.c2 = 0

        # Integers / ptrs we need.
        self.buf_ptr = 0
        self.i = 0
        self.j = 0
        # Assorted flags
        self.csum = 0
        self.ml = 0
        self.m = 0
        self.k = 0
        self.hd = 0
        self.utf8 = 0
        self.len = 0

    def decode(self, buf):
        """

        :param buf:
        :return:
        """
        self.reset()
        self.buf = buf
        while self.state:
            # Loop prolog
            r = self.loop_prolog()
            if r == c.PROLOG_BREAK:
                break
            if r == c.PROLOG_CONTINUE:
                continue
            # Now we handle states!
            func = self.state_to_func.get(self.state)
            if not func:
                raise exc.InternalError('Illegal state found: {}'.format(self.state))
            func()
        log.info('Out of while loop')
        # flush out the out_buf to output_buf
        log.info(self.j)
        log.info(len(self.out_buf))
        self.output_buf += self.out_buf


    def loop_prolog(self):
        # log.debug('Loop prolog')
        # Update input buffer
        # if not self.in_buf or self.in_buf[self.i] == 0x00:
        if not self.in_buf or self.i == len(self.in_buf):
            log.debug('Evaluating in_buf conditions')
            if self.buf_ptr > len(self.buf):
                log.debug('End of input buf')
                if self.len:
                    log.error('Premature end of buf')
                    if self.utf8 > 0:
                        log.error('The file seems to contain special characters, try the -cp option.')
                return c.PROLOG_BREAK
            else:
                # Populate self.in_buf by c.LEN_OUTBUF chars
                self.in_buf = self.buf[self.buf_ptr: self.buf_ptr + c.LEN_INBUF]
                log.debug('Updating in_buf - populated {} characters'.format(len(self.in_buf)))
                self.buf_ptr = self.buf_ptr + c.LEN_INBUF
                self.i = 0
                return c.PROLOG_CONTINUE
        # Update output buffer
        if self.j == c.LEN_OUTBUF:
            log.debug('Updating out_buf')
            self.output_buf += self.out_buf
            # Reset the out_buf to be empty
            self.out_buf = ''
            self.j = 0
        # Handle urlencoded states
        if self.url_encoded == 1 and self.in_buf[self.i] == '%':
            log.debug('Saving urlencoding state')
            self.ustate = self.state
            self.state = c.STATE_URLENCODE_1
            self.i += 1
            return c.PROLOG_CONTINUE
        # 2 means we do urldecoding but wanted to avoid decoding an
        # already decoded % for the second time
        if self.url_encoded == 2:
            log.debug('self.url_encoded 2->1')
            self.url_encoded = 1
        # Handle htmlencoded states
        if self.html_encoded == 1 and self.in_buf[self.i] == '%':
            log.debug('Saving htmlencoding state')
            self.ustate = self.state
            self.state = c.STATE_HTMLENCODE
            self.hd = 0
            self.i += 1
            return c.PROLOG_CONTINUE
        # 2 means we do htmldecoding but wanted to avoid decoding an
        # already decoded % for the second time
        if self.html_encoded == 2:
            log.debug('self.html_encoded 2->1')
            self.html_encoded = 1
        return c.PROLOG_NO_ACTION

    def state_htmlencode(self):
        log.debug('state_htmlencode')
        self.c1 = self.in_buf[self.i]
        if self.c1 != ';':
            self.i += 1
            self.htmldec += self.c1
            self.hd += 1
            if self.hd > 7:
                log.error('HTML decode encountered a too long mnemonic: {}'.format(self.htmldec))
                raise exc.InternalError('Invalid html mnemonic found')
        else:
            # ';' means we are at the end of the mnemonic
            c1 = utility.decode_mnemonic(self.htmldec)
            # Copy the decoded character back into the input buffer
            self.in_buf = self.in_buf[:self.i] + c1 + self.in_buf[self.i+1:]
            self.html_encoded = 2
            self.state = self.ustate

    def state_urlencode_2(self):
        log.debug('state_urlencode_2')
        self.c2 = ord(self.in_buf[self.i]) - 0x30
        if self.c2 > 0x9:
            self.c2 -= 0x7
        if self.c2 > 0x10:
            self.c2 -= 0x20
        c2 = chr(self.c2 + (self.c << 4))
        # Copy the decoded character back into the input buffer
        self.in_buf = self.in_buf[:self.i] + c2 + self.in_buf[self.i+1:]
        # avoid looping in case this was an %
        self.url_encoded = 2
        # Restore old state
        self.state = self.ustate

    def state_urlencode_1(self):
        log.debug('state_urlencode_1')
        self.c1 = ord(self.in_buf[self.i]) - 0x30
        self.i += 1
        if self.c1 > 0x9:
            self.c1 -= 0x7
        if self.c1 > 0x10:
            self.c1 -= 0x20
        self.state = c.STATE_URLENCODE_2

    def state_readlen(self):
        log.debug('state_readlen')
        self.len_buf += self.in_buf[self.i]
        self.i += 1
        self.ml -= 1
        if not self.ml:
            self.len = utility.decode_base64(chars=self.len_buf,
                                     digits=self.digits)
            log.debug('Found encoded block containing {} characters'.format(self.len))
            self.m = 0
            self.ml = 2
            self.state = c.STATE_SKIP_ML
            self.nextstate = c.STATE_DECODE

    def state_checksum(self):
        log.debug('state_checksum')
        self.csbuf += self.in_buf[self.i]
        self.i += 1
        self.ml -= 1
        if not self.ml:
            self.csum = utility.decode_base64(chars=self.csbuf, digits=self.digits)
            if self.csum:
                log.error('Incorrect checksum: {}'.format(self.csum))
                # XXX
                log.error(repr(self))
                if self.codepage:
                    log.warning('Possibly try a different codepage')
                else:
                    if self.utf8 > 0:
                        log.warning('The file seems to contain special characters')
                    else:
                        log.warning('The file may be corrupted')
                self.csum = 0
            else:
                log.debug('Checksum OK')
            self.m = 0
            self.ml = 6
            self.state = c.STATE_SKIP_ML
            if self.smart:
                self.nextstate = c.STATE_WAIT_FOR_CLOSE
            else:
                self.nextstate = c.STATE_INIT_COPY

    def state_unescape(self):
        # log.debug('state_unescape')
        _c = utility.unescape(self.in_buf[self.i])
        self.out_buf += _c
        self.j += 1
        self.i += 1

        self.len -= 1
        self.m += 1
        self.state = c.STATE_DECODE

    def state_dbcs(self):
        log.debug('state_dbcs')
        self.out_buf += self.in_buf[self.i]
        self.j += 1
        self.i += 1
        self.state = c.STATE_DECODE

    def state_decode(self):
        # log.debug('state_decode')
        if not self.len:
            self.ml = 6
            self.state = c.STATE_CHECKSUM
            return
        if self.in_buf[self.i] == '@':
            self.state = c.STATE_UNESCAPE
        else:
            if (ord(self.in_buf[self.i]) & 0x80) == 0:
                encoding_index = self.m % 64
                encoding_index2 = c.PICK_ENCODING[encoding_index]
                _c = self.transform_map[encoding_index2].get(ord(self.in_buf[self.i]))
                # XXX
                # log.debug(_c)
                self.out_buf += chr(_c)
                self.csum += _c
                self.m += 1

            else:
                if not self.codepage and ((ord(self.in_buf[self.i]) & 0x80) == 0x80):
                    # UTF-8 but not a start byte
                    self.len += 1
                    self.utf8 = 1
                self.out_buf += self.in_buf[self.i]
                self.j += 1
                if self.codepage and utility.is_lead_byte(self.codepage, ord(self.in_buf[self.i])):
                    self.state = c.STATE_DBCS
        self.i += 1
        self.len -= 1

    def state_init_readlen(self):
        log.debug('state_init_readlen')
        self.ml = 6
        self.state = c.STATE_READLEN

    def state_skip_ml(self):
        log.debug('state_skip_ml')
        self.i += 1
        self.ml -= 1
        if not self.ml:
            self.state = self.nextstate

    def state_flushing(self):
        log.debug('state_flushing')
        self.out_buf += c.MARKER[self.k]
        self.j += 1
        self.k += 1
        self.m -= 1
        if self.m == 0:
            self.state = c.STATE_COPY_INPUT

    def state_copy_input(self):
        log.debug('state_copy_input')
        if self.in_buf[self.i] == c.MARKER[self.m]:
            self.i += 1
            self.m += 1
        else:
            if self.m:
                self.k = 0
                self.state = c.STATE_FLUSHING
            else:
                self.out_buf += self.in_buf[self.i]
                self.j += 1
                self.i += 1
        if self.m == self.ml:
            self.state = c.STATE_INIT_READLEN

    def state_wait_for_open(self):
        log.debug('state_wait_for_open')
        if self.in_buf[self.i] == '<':
            self.state = c.STATE_INIT_COPY
        self.out_buf += self.in_buf[self.i]
        self.j += 1
        self.i += 1

    def state_wait_for_close(self):
        log.debug('state_wait_for_close')
        if self.in_buf[self.i] == '>':
            self.state = c.STATE_WAIT_FOR_OPEN
        self.out_buf += self.in_buf[self.i]
        self.j += 1
        self.i += 1

    def state_init_copy(self):
        log.debug('state_init_copy')
        self.ml = len(c.MARKER)
        self.m = 0
        self.state = c.STATE_COPY_INPUT

