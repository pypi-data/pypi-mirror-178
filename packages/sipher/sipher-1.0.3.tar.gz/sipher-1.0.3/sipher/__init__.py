"""Encrypt/Decrypt message using morse/rsa/base64"""

from ._rsa import RSA
from ._base64 import Base64
from ._morse import Morse

rsa = RSA()
base64 = Base64()
morse = Morse()

__author__ = 'srg'
__version__ = '1.0.3'

__all__ = [
    'rsa',
    'base64',
    'morse'
]
