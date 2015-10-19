"""
exc.py from vbe_decoder
Created: 10/18/15

Purpose: Exceptions for the decoder.
"""
# Stdlib
from __future__ import print_function
import logging
import os
import sys
# Third Party code
# Custom Code
log = logging.getLogger(__name__)
__author__ = 'wgibb'
__version__ = '0.0.1'

class DecodeError(Exception):
    """
    General error with the decoder.
    """
    pass


class InternalError(DecodeError):
    """
    Some internal constraint was violated.
    """
    pass


