"""
exc.py from vbe_decoder
Created: 10/18/15

Purpose: Exceptions for the decoder.
"""


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


