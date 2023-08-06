from __future__ import annotations

import os
import sys
import argparse
from srutil import util
from pathlib import Path

from ._sipher import Sipher
from . import rsa, base64, morse, __version__, __package__


def get_argument():
    parser = argparse.ArgumentParser(prog=__package__, usage=util.stringbuilder(__package__, " [options]"))
    parser.add_argument('-v', '--version', action='version', help='show version number and exit.', version=__version__)
    group = parser.add_argument_group("to encrypt/decrypt message")
    group.add_argument("data", type=str, help="data to encrypt/decrypt")
    group.add_argument("-k", "--key", dest='key', metavar='', default=rsa.load_keys(),
                       help=argparse.SUPPRESS)
    group.add_argument("-a", "--alg", dest='alg', metavar='', choices=['morse', 'base64', 'rsa'], type=str,
                       required=True, help="algorithm to use")
    group.add_argument("-e", "--encrypt", dest="encrypt", default=False, action="store_true",
                       help="to encrypt message")
    group.add_argument("-d", "--decrypt", dest="decrypt", default=False, action="store_true",
                       help="to decrypt message")
    group.add_argument("-c", "--copy", dest="copy_to_clipboard", default=False, action="store_true",
                       help="to copy encrypted/decrypted message to clipboard (default : %(default)s)")
    group.add_argument("-s", "--store", dest="store", default=False, action="store_true",
                       help="to store encrypted/decrypted message as text file (default : %(default)s)")
    group.add_argument("-p", "--path", dest="store_path", default=os.getcwd(), metavar='',
                       help="path to store encrypted/decrypted message")
    parser.add_argument_group(group)
    options = parser.parse_args()
    if not options.encrypt and not options.decrypt:
        parser.error("one of the following arguments are required: -e/--encrypt or -d/--decrypt")
    if options.encrypt and options.decrypt:
        parser.error("any one of the following arguments should be given: -e/--encrypt or -d/--decrypt")
    if not options.copy_to_clipboard and not options.store:
        parser.error("one of the following arguments are required: -c/--copy or -s/--store")
    return options


def _remove_unwanted_params(s: Sipher, params: dict) -> dict:
    method_list = {'encrypt': s.encrypt, 'decrypt': s.decrypt}
    params_of_method = util.paramsofmethod(method_list.get(util.whocalledme())).keys()
    new_params = dict()
    for key, value in params.items():
        if key in params_of_method:
            new_params.setdefault(key, value)
    return new_params


def encrypt(s: Sipher, data: str | os.PathLike, **kwargs):
    kwargs = _remove_unwanted_params(s, kwargs)
    s.encrypt(data, **kwargs)


def decrypt(s: Sipher, data: str | os.PathLike, **kwargs):
    kwargs = _remove_unwanted_params(s, kwargs)
    s.decrypt(data, **kwargs)


def main():
    options = get_argument()
    sipher_alg = {'morse': morse, 'rsa': rsa, 'base64': base64}
    s = sipher_alg.get(options.alg)
    data = Path(options.data) if os.path.exists(options.data) else options.data
    if options.encrypt:
        encrypt(s, data, pub_key=options.key.__getitem__(1), copy_to_clipboard=options.copy_to_clipboard,
                store=options.store, store_path=options.store_path)
    elif options.decrypt:
        decrypt(s, data, priv_key=options.key.__getitem__(0), copy_to_clipboard=options.copy_to_clipboard,
                store=options.store, store_path=options.store_path)


if __name__ == "__main__":
    sys.exit(main())
