
from __future__ import print_function as _
import sys as _sys

import tcod as _tcod
from . import Color as _Color
from .libtcod import _lib, _ffi, _int, _str, _unicode

_numpy = None

def _numpy_available():
    'check if numpy is available and lazily load it when needed'
    global _numpy
    if _numpy is None:
        try:
            import numpy as _numpy
        except ImportError:
            _numpy = False
    return _numpy

# initializing the console
def init_root(w, h, title, fullscreen=False, renderer=_tcod.RENDERER_SDL):
    _lib.TCOD_console_init_root(w, h, _str(title), fullscreen, renderer)
    

def set_custom_font(fontFile, flags=_tcod.FONT_LAYOUT_ASCII_INCOL,
                            nb_char_horiz=0, nb_char_vertic=0):
    _lib.TCOD_console_set_custom_font(fontFile, flags,
                                     nb_char_horiz, nb_char_vertic)


def get_width(con):
    return _lib.TCOD_console_get_width(con or _ffi.NULL)

def get_height(con):
    return _lib.TCOD_console_get_height(con or _ffi.NULL)

def set_custom_font(fontFile, flags=_tcod.FONT_LAYOUT_ASCII_INCOL,
                            nb_char_horiz=0, nb_char_vertic=0):
    _lib.TCOD_console_set_custom_font(_str(fontFile), flags,
                                      nb_char_horiz, nb_char_vertic)

def map_ascii_code_to_font(asciiCode, fontCharX, fontCharY):
    _lib.TCOD_console_map_ascii_code_to_font(_int(asciiCode), fontCharX,
                                                              fontCharY)

def map_ascii_codes_to_font(firstAsciiCode, nbCodes, fontCharX,
                                    fontCharY):
    _lib.TCOD_console_map_ascii_codes_to_font(_int(firstAsciiCode), nbCodes,
                                              fontCharX, fontCharY)

def map_string_to_font(s, fontCharX, fontCharY):
    _lib.TCOD_console_map_string_to_font_utf(_unicode(s), fontCharX, fontCharY)

def is_fullscreen():
    return _lib.TCOD_console_is_fullscreen()

def set_fullscreen(fullscreen):
    _lib.TCOD_console_set_fullscreen(fullscreen)

def is_window_closed():
    return _lib.TCOD_console_is_window_closed()

def set_window_title(title):
    _lib.TCOD_console_set_window_title(_str(title))

def credits():
    _lib.TCOD_console_credits()

def credits_reset():
    _lib.TCOD_console_credits_reset()

def credits_render(x, y, alpha):
    return _lib.TCOD_console_credits_render(x, y, alpha)

def flush():
    _lib.TCOD_console_flush()

# drawing on a console
def set_default_background(con, col):
    _lib.TCOD_console_set_default_background(con or _ffi.NULL, col)

def set_default_foreground(con, col):
    _lib.TCOD_console_set_default_foreground(con or _ffi.NULL, col)

def clear(con):
    return _lib.TCOD_console_clear(con or _ffi.NULL)

def put_char(con, x, y, c, flag=_tcod.BKGND_DEFAULT):
    _lib.TCOD_console_put_char(con or _ffi.NULL, x, y, _int(c), flag)

def put_char_ex(con, x, y, c, fore, back):
    _lib.TCOD_console_put_char_ex(con or _ffi.NULL, x, y, _int(c), fore, back)

def set_char_background(con, x, y, col, flag=_tcod.BKGND_SET):
    _lib.TCOD_console_set_char_background(con or _ffi.NULL, x, y, col, flag)

def set_char_foreground(con, x, y, col):
    _lib.TCOD_console_set_char_foreground(con or _ffi.NULL, x, y, col)

def set_char(con, x, y, c):
    _lib.TCOD_console_set_char(con or _ffi.NULL, x, y, _int(c))

def set_background_flag(con, flag):
    _lib.TCOD_console_set_background_flag(con or _ffi.NULL, flag)

def get_background_flag(con):
    return _lib.TCOD_console_get_background_flag(con or _ffi.NULL)

def set_alignment(con, alignment):
    _lib.TCOD_console_set_alignment(con or _ffi.NULL, alignment)

def get_alignment(con):
    return _lib.TCOD_console_get_alignment(con or _ffi.NULL)

_print = print
def print(con, x, y, fmt):
    _lib.TCOD_console_print_utf(con or _ffi.NULL, x, y, _unicode(fmt))

def print_ex(con, x, y, flag, alignment, fmt):
    _lib.TCOD_console_print_ex_utf(con or _ffi.NULL, x, y,
                                   flag, alignment, _unicode(fmt))

def print_rect(con, x, y, w, h, fmt):
    return _lib.TCOD_console_print_rect_utf(con or _ffi.NULL, x, y, w, h,
                                            _unicode(fmt))

def print_rect_ex(con, x, y, w, h, flag, alignment, fmt):
    _lib.TCOD_console_print_rect_ex_utf(con or _ffi.NULL, x, y, w, h, flag,
                                        alignment, _unicode(fmt))

def get_height_rect(con, x, y, w, h, fmt):
    return _lib.TCOD_console_get_height_rect_utf(con or _ffi.NULL, x, y, w, h,
                                                 _unicode(fmt))

def rect(con, x, y, w, h, clr, flag=_tcod.BKGND_DEFAULT):
    _lib.TCOD_console_rect(con or _ffi.NULL, x, y, w, h, clr, flag)

def hline(con, x, y, l, flag=_tcod.BKGND_DEFAULT):
    _lib.TCOD_console_hline(con or _ffi.NULL, x, y, l, flag)

def vline(con, x, y, l, flag=_tcod.BKGND_DEFAULT):
    _lib.TCOD_console_vline(con or _ffi.NULL, x, y, l, flag)

def print_frame(con, x, y, w, h, clear=True, flag=_tcod.BKGND_DEFAULT, fmt=b''):
    _lib.TCOD_console_print_frame(con or _ffi.NULL, x, y, w, h, clear, flag,
                                  _str(fmt))

def set_color_control(con, fore, back) :
    _lib.TCOD_console_set_color_control(con or _ffi.NULL, fore, back)

def get_default_background(con):
    return _Color.from_cdata(_lib.TCOD_console_get_default_background(con or _ffi.NULL))

def get_default_foreground(con):
    return _Color.from_cdata(_lib.TCOD_console_get_default_foreground(con or _ffi.NULL))

def get_char_background(con, x, y):
    return _Color.from_cdata(_lib.TCOD_console_get_char_background(con or _ffi.NULL, x, y))

def get_char_foreground(con, x, y):
    return _Color.from_cdata(_lib.TCOD_console_get_char_foreground(con or _ffi.NULL, x, y))

def get_char(con, x, y):
    return _lib.TCOD_console_get_char(con or _ffi.NULL, x, y)

def set_fade(fade, fadingColor):
    _lib.TCOD_console_set_fade(fade, fadingColor)

def get_fade():
    return _lib.TCOD_console_get_fade()

def get_fading_color():
    return _Color.from_cdata(_lib.TCOD_console_get_fading_color())

# handling keyboard input
def wait_for_keypress(flush):
    k=_tcod.Key()
    _lib.TCOD_console_wait_for_keypress_wrapper(k._struct, flush)
    return k

def check_for_keypress(flags=_tcod.KEY_RELEASED):
    k=_tcod.Key()
    _lib.TCOD_console_check_for_keypress_wrapper(k._struct, flags)
    return k

def is_key_pressed(key):
    return _lib.TCOD_console_is_key_pressed(key)

def set_keyboard_repeat(initial_delay, interval):
    _lib.TCOD_console_set_keyboard_repeat(initial_delay, interval)

def disable_keyboard_repeat():
    _lib.TCOD_console_disable_keyboard_repeat()

# using offscreen consoles
def new(w, h):
    return _lib.TCOD_console_new(w, h)
def from_file(filename):
    return _lib.TCOD_console_from_file(_str(filename))
def get_width(con):
    return _lib.TCOD_console_get_width(con or _ffi.NULL)

def get_height(con):
    return _lib.TCOD_console_get_height(con or _ffi.NULL)

def blit(src, x, y, w, h, dst, xdst, ydst, ffade=1.0,bfade=1.0):
    _lib.TCOD_console_blit(src or _ffi.NULL, x, y, w, h, dst or _ffi.NULL,
                           xdst, ydst, ffade, bfade)

def set_key_color(con, col):
    _lib.TCOD_console_set_key_color(con or _ffi.NULL, col)

def delete(con):
    _lib.TCOD_console_delete(con or _ffi.NULL)

# fast color filling
def fill_foreground(con,r,g,b) :
    if len(r) != len(g) or len(r) != len(b):
        raise TypeError('R, G and B must all have the same size.')
    numpy_available = False
    if (numpy_available and isinstance(r, _numpy.ndarray) and
        isinstance(g, _numpy.ndarray) and isinstance(b, _numpy.ndarray)):
        #numpy arrays, use numpy's ctypes functions
        r = _numpy.ascontiguousarray(r, dtype=_numpy.int_)
        g = _numpy.ascontiguousarray(g, dtype=_numpy.int_)
        b = _numpy.ascontiguousarray(b, dtype=_numpy.int_)
        cr = _ffi.cast('int *', r.ctypes.data)
        cg = _ffi.cast('int *', g.ctypes.data)
        cb = _ffi.cast('int *', b.ctypes.data)
    else:
        # otherwise convert using ffi arrays
        cr = _ffi.new('int[]', r)
        cg = _ffi.new('int[]', g)
        cb = _ffi.new('int[]', b)

    _lib.TCOD_console_fill_foreground(con or _ffi.NULL, cr, cg, cb)

def fill_background(con,r,g,b) :
    if len(r) != len(g) or len(r) != len(b):
        raise TypeError('R, G and B must all have the same size.')
    if (_numpy_available() and isinstance(r, _numpy.ndarray) and
        isinstance(g, _numpy.ndarray) and isinstance(b, _numpy.ndarray)):
        #numpy arrays, use numpy's ctypes functions
        r = _numpy.ascontiguousarray(r, dtype=_numpy.int_)
        g = _numpy.ascontiguousarray(g, dtype=_numpy.int_)
        b = _numpy.ascontiguousarray(b, dtype=_numpy.int_)
        cr = _ffi.cast('int *', r.ctypes.data)
        cg = _ffi.cast('int *', g.ctypes.data)
        cb = _ffi.cast('int *', b.ctypes.data)
    else:
        # otherwise convert using ffi arrays
        cr = _ffi.new('int[]', r)
        cg = _ffi.new('int[]', g)
        cb = _ffi.new('int[]', b)

    _lib.TCOD_console_fill_background(con or _ffi.NULL, cr, cg, cb)

def fill_char(con,arr) :
    if (_numpy_available() and isinstance(arr, _numpy.ndarray) ):
        #numpy arrays, use numpy's ctypes functions
        arr = numpy.ascontiguousarray(arr, dtype=_numpy.int_)
        carr = _ffi.cast('int *', arr.ctypes.data)
    else:
        #otherwise convert using the ffi module
        carr = _ffi.new('int[]', arr)

    _lib.TCOD_console_fill_char(con or _ffi.NULL, carr)
        
def load_asc(con, filename) :
    _lib.TCOD_console_load_asc(con or _ffi.NULL, _str(filename))
def save_asc(con, filename) :
    _lib.TCOD_console_save_asc(con or _ffi.NULL,_str(filename))
def load_apf(con, filename) :
    _lib.TCOD_console_load_apf(con or _ffi.NULL,_str(filename))
def save_apf(con, filename) :
    _lib.TCOD_console_save_apf(con or _ffi.NULL,_str(filename))

__all__ = [_name for _name in list(globals()) if _name[0] != '_']
