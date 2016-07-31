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
from vbe_decoder.decoder import Decoder
from vbe_decoder.exc import DecodeError, InternalError
__all__ = ['Decoder', 'DecodeError', 'InternalError']
__author__ = 'william.gibb'
__version__ = '0.1.0'

log = logging.getLogger(__name__)
