from __future__ import annotations

import os
import abc
from srutil import util
from typing import AnyStr

from . import sipherutil as su


class Sipher:

    @staticmethod
    def _get_data_from_file(file: os.PathLike[AnyStr], mode='r') -> AnyStr:
        path = file.__str__().replace("\\", "/")
        file_name = os.path.basename(path)
        data_path = path.replace(util.stringbuilder('/', file_name), "")
        data = su.retrieve(path=data_path, file_name=file_name, mode=mode)
        return data

    @staticmethod
    def _copy_store_m(m, alg, copy: bool = False, store: bool = False, store_path=None, mode='w',
                      encryption: bool = False, decryption: bool = False) -> None:
        msg = "Encrypted" if encryption else "Decrypted" if decryption else ''
        if copy is True:
            is_copied = su.copy_to_clipboard(m)
            if is_copied:
                print("{} message copied to clipboard.".format(msg).strip())
        if store is True:
            path = su.store(data=m, path=store_path, alg=alg.__class__.__name__.lower(), mode=mode)
            if path.exists():
                print("{} message stored in '{}'".format(msg, path.__str__()).strip())

    @abc.abstractmethod
    def encrypt(self, data: AnyStr | os.PathLike[AnyStr], **kwargs) -> AnyStr:
        pass

    @abc.abstractmethod
    def decrypt(self, data: AnyStr | os.PathLike[AnyStr], **kwargs) -> AnyStr:
        pass
