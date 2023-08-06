from __future__ import annotations

import rsa
import os.path
from os import PathLike
from srutil import util
from pathlib import Path
from rsa import PublicKey, PrivateKey
from typing import AnyStr, Optional, Tuple

from ._sipher import Sipher
from . import sipherutil as su


class RSA(Sipher):
    def __init__(self):
        self.__home_path = util.stringbuilder(su.home(), 'rsa', separator='/')
        self.__em = ''
        self.__dm = ''

    @staticmethod
    def _new_keys(n: int) -> Tuple[PublicKey, PrivateKey]:
        return rsa.newkeys(nbits=n)

    def gen_keys(self, force_gen: bool = False) -> None:
        public, private = RSA._new_keys(1024)
        if not os.path.exists(self.__home_path):
            os.mkdir(util.getinstanceof(self.__home_path, Path))
        path = util.stringbuilder(self.__home_path, 'keys', separator='/')
        if os.path.exists(path) and not force_gen:
            return
        if not os.path.exists(path):
            os.mkdir(util.getinstanceof(path, Path))
        su.store(data=public.save_pkcs1('PEM'), path=path, file_name='publicKey', file_format='pem', mode='wb')
        su.store(data=private.save_pkcs1('PEM'), path=path, file_name='privateKey', file_format='pem', mode='wb')

    def load_keys(self) -> Tuple[PrivateKey, PublicKey]:
        self.gen_keys()
        path = util.stringbuilder(self.__home_path, 'keys', separator='/')
        public = rsa.PublicKey.load_pkcs1(su.retrieve(path=path, file_name='publicKey', file_format='pem', mode='rb'))
        private = rsa.PrivateKey.load_pkcs1(
            su.retrieve(path=path, file_name='privateKey', file_format='pem', mode='rb'))
        return private, public

    def sign(self, message: AnyStr | PathLike[AnyStr], priv_key: PrivateKey) -> bytes:
        if isinstance(message, PathLike):
            message = self._get_data_from_file(message)
        return rsa.sign(message=message.encode('ascii'), priv_key=priv_key, hash_method='SHA-1')

    def verify(self, message: bytes, signature: bytes, pub_key: PublicKey) -> str:
        if not message:
            message = self.__dm
        return rsa.verify(message=message, signature=signature, pub_key=pub_key)

    def encrypt(self, data: AnyStr | PathLike[AnyStr], pub_key: PublicKey = None, copy_to_clipboard: bool = False,
                store: bool = False, store_path: Optional[str] = None) -> bytes:
        if isinstance(data, PathLike):
            data = self._get_data_from_file(data)
        self.__em = rsa.encrypt(data.encode('ascii'), pub_key=pub_key)
        self._copy_store_m(self.__em, self, copy_to_clipboard, store, store_path, 'wb', encryption=True)
        return self.__em

    def decrypt(self, data: bytes | PathLike[bytes], priv_key: PrivateKey = None, copy_to_clipboard: bool = False,
                store: bool = False, store_path: Optional[str] = None) -> str:
        if isinstance(data, PathLike):
            data = self._get_data_from_file(data, mode='rb')
        self.__dm = rsa.decrypt(data, priv_key=priv_key)
        self._copy_store_m(self.__dm, self, copy_to_clipboard, store, store_path, 'wb', decryption=True)
        return self.__dm.decode('ascii')
