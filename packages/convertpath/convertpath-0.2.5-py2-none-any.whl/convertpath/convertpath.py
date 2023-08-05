import os
import re
from pathlib import Path, PurePosixPath, PureWindowsPath

class convertpath:

    def __init__(self, path=os.environ['HOME']):
        self.path = path

    def win2linux(self, path=None):
        rawpath = path or self.path
        rst = convertpath_win2linux(rawpath)
        return rst

    def linux2win(self, path=None):
        rawpath = path or self.path
        rst = convertpath_linux2win(rawpath)
        return rst


def convertpath_win2linux(path):
    """ Convert a directory path from windows path to linux path

    >>> convertpath_win2linux(r"C:\\Users\\user")
    '/C/Users/user'
    """

    rst = PurePosixPath(Path(path))
    rst = re.sub(r'^C:\\', r'/C', str(rst))
    rst = re.sub(r'^c:\\', r'/c', str(rst))
    return str(rst)


def convertpath_linux2win(path):
    """ Convert a directory path from linux path to windows path

    >>> convertpath_linux2win(r"/C/Users/user")
    'C:\\\\Users\\\\user'
    """
    
    path = re.sub(r'^/[Cc]', r'', str(path))
    rst = PureWindowsPath(Path(path))
    return str(rst)
