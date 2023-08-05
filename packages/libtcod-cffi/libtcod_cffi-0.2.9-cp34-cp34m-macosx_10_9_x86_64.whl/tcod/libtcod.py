
import os as _os
import sys as _sys

import ctypes as _ctypes
import platform as _platform

from . import __path__

def _get_lib_path_crossplatform():
    '''Locate the right DLL path for this OS'''
    bits, linkage = _platform.architecture()
    if 'win32' in _sys.platform:
        return 'lib/win32/'
    elif 'linux' in _sys.platform:
        if bits == '32bit':
            return 'lib/linux32/'
        elif bits == '64bit':
            return 'lib/linux64/'
    elif 'darwin' in _sys.platform:
        return 'lib/darwin/'
    raise ImportError('Operating system "%s" has no supported dynamic link libarary. (%s, %s)' % (_sys.platform, bits, linkage))

def _get_lib_name():
    bits, linkage = _platform.architecture()
    if 'win32' in _sys.platform:
        return 'libtcod-VS.dll'
    elif 'linux' in _sys.platform:
        return 'libtcod.so'
    elif 'darwin' in _sys.platform:
        return 'libtcod.dylib'

# add Windows dll's to PATH
if 'win' in _sys.platform:
    _os.environ['PATH'] += ';' + _os.path.join(__path__[0],
                                               _get_lib_path_crossplatform())

# add Mac dylib's to DYLD_LIBRARY_PATH
if 'darwin' in _sys.platform:
    _os.environ['DYLD_LIBRARY_PATH'] = _os.path.join(__path__[0],
                                                _get_lib_path_crossplatform())

_lib_ctypes = _ctypes.CDLL(
    _os.path.realpath(
        _os.path.join(__path__[0],
            _get_lib_path_crossplatform(), _get_lib_name())))

from . import _libtcod

_ffi = ffi = _libtcod.ffi
_lib = lib = _libtcod.lib

def _unpack_char_p(char_p):
    return ffi.string(char_p).decode()

def _int(int_or_str):
    'return an integer where a signle character string may be expected'
    if isinstance(int_or_str, str):
        return ord(int_or_str)
    if isinstance(int_or_str, bytes):
        return int_or_str[0]
    return int(int_or_str)

if _sys.version_info[0] == 2: # Python 2
    def _str(string):
        if isinstance(string, unicode):
            return string.encode()
        return string

    def _unicode(string):
        if not isinstance(string, unicode):
            return string.decode()
        return string

else: # Python 3
    def _str(string):
        if isinstance(string, str):
            return string.encode()
        return string

    def _unicode(string):
        if isinstance(string, bytes):
            return string.decode()
        return string

