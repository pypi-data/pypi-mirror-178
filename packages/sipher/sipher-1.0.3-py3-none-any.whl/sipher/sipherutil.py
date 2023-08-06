import os
from pathlib import Path
from srutil import util
from typing import Optional, AnyStr


def home() -> str:
    path = util.stringbuilder(util.home(), '/.sipher')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def store(data: AnyStr, file_name: Optional[str] = None, path: Optional[str] = None, file_format: Optional[str] = None,
          alg: Optional[str] = None, mode: str = 'w') -> Path:
    if not path:
        path = os.getcwd()
    if not file_name:
        if not alg:
            alg = ''
        file_name = "{}_{}".format(alg, util.epoch())
    if not file_format:
        file_format = 'txt'
    path += "/{}.{}".format(file_name, file_format)
    file = Path(path)
    with open(file, mode) as f:
        f.write(data)
    return file


def retrieve(file_name: str, path: str, file_format: str = None, mode: str = 'r') -> AnyStr:
    if not path:
        path = os.getcwd()
    if not file_format:
        file_format = ''
    path += "/{}.{}".format(file_name, file_format).rstrip('.')
    file = Path(path)
    with open(file, mode) as f:
        to_return = f.read()
    return to_return


def copy_to_clipboard(text) -> bool:
    return util.to_clipboard(text)
