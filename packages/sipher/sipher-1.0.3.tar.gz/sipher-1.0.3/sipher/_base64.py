from __future__ import annotations

import os
import base64
from typing import AnyStr, Optional

from sipher._sipher import Sipher


class Base64(Sipher):
    def __init__(self):
        self.__em = ''
        self.__dm = ''

    def encrypt(self, data: AnyStr | os.PathLike[AnyStr], copy_to_clipboard: bool = False,
                store: bool = False, store_path: Optional[str] = None):
        if isinstance(data, os.PathLike):
            data = self._get_data_from_file(data)
        base64_bytes = base64.b64encode(data.encode('ascii'))
        self.__em = base64_bytes.decode('ascii')
        self._copy_store_m(self.__em, self, copy_to_clipboard, store, store_path, encryption=True)
        return self.__em

    def decrypt(self, data: AnyStr | os.PathLike[AnyStr], copy_to_clipboard: bool = False,
                store: bool = False, store_path: Optional[str] = None):
        if isinstance(data, os.PathLike):
            data = self._get_data_from_file(data)
        data_bytes = base64.b64decode(data.encode('ascii'))
        self.__dm = data_bytes.decode('ascii')
        self._copy_store_m(self.__dm, self, copy_to_clipboard, store, store_path, decryption=True)
        return self.__dm
