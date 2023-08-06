#!/usr/bin/env python3

import os
import sys

import platform
from pycparser import c_parser, c_ast, parse_file, c_generator
from cffi import FFI

BITSIZE, LINKAGE = platform.architecture()

def _get_library_dirs_crossplatform():
    if 'win32' in sys.platform:
        return ['src/lib/win32/']
    elif 'linux' in sys.platform:
        if BITSIZE == '32bit':
            return ['src/lib/linux32/']
        elif BITSIZE == '64bit':
            return ['src/lib/linux64/']
    elif 'darwin' in sys.platform:
        return ['src/SDL.framework/Versions/A/']
    raise ImportError('Operating system "%s" has no supported dynamic link libarary. (%s, %s)' % (sys.platform, BITSIZE, LINKAGE))

def _get_libraries_crossplatform():
    return ['SDL', 'OpenGL32']
    if sys.platform == 'win32':
        return ['libtcod-VS']
    elif 'linux' in sys.platform:
        return ['tcod']
    elif 'darwin' in sys.platform:
        return ['tcod']
    raise ImportError('Operating system "%s" has no supported dynamic link libarary. (%s, %s)' % (sys.platform, BITSIZE, LINKAGE))


def walk_sources(directory):
    for path, dirs, files in os.walk(directory):
        for source in files:
            if not source.endswith('.c'):
                continue
            yield os.path.join(path, source)

def find_sources(directory):
    return [os.path.join(directory, source)
            for source in os.listdir(directory)
            if source.endswith('.c')]

module_name = 'tcod._libtcod'
include_dirs = ['Release/tcod/',
                'dependencies/libtcod-1.5.1/include/',
                'dependencies/libtcod-1.5.1/src/png/']
extra_compile_args = []
extra_link_args = []
sources = []

sources += [file for file in walk_sources('dependencies/libtcod-1.5.1/src')
            if 'sys_sfml_c' not in file]
sources += find_sources('dependencies/zlib-1.2.8/')

libraries = []
library_dirs = []
define_macros = [('LIBTCOD_EXPORTS', None)]

with open('src/tdl_source.c', 'r') as file_source:
    source = file_source.read()

if sys.platform == 'win32':
    libraries += ['User32', 'OpenGL32']

if 'linux' in sys.platform:
    libraries += ['GL']

if sys.platform == 'darwin':
    extra_link_args += ['-framework', 'OpenGL']

libraries += ['SDL']

# included SDL headers are for whatever OS's don't easily come with them
if sys.platform in ['win32', 'darwin']:
    include_dirs += ['dependencies/SDL-1.2.15/include', 'dependencies/zlib-1.2.8/']

    if BITSIZE == '32bit':
        library_dirs += [os.path.realpath('dependencies/SDL-1.2.15/lib/x86')]
    else:
        library_dirs += [os.path.realpath('dependencies/SDL-1.2.15/lib/x64')]

def get_cdef():
    generator = c_generator.CGenerator()
    return generator.visit(get_ast())

def get_ast():
    ast = parse_file(filename='src/libtcod_cdef.h', use_cpp=True,
                     cpp_args=[r'-Idependencies/fake_libc_include',
                               r'-Idependencies/libtcod-1.5.1/include',
                               r'-DDECLSPEC=',
                               r'-DSDLCALL=',
                               r'-DTCODLIB_API=',
                               ])
    for node in list(ast.ext):
        # resolve binary ops in TCOD_event_t enum
        if not isinstance(node, c_ast.Typedef):
            continue
        if node.name == 'wchar_t':
            ast.ext.remove(node) # remove wchar_t placeholder
        if node.name != 'TCOD_event_t':
            continue

        # get to enumerator list node
        (type, node), = node.children()
        (type, node), = node.children()
        (type, node), = node.children()

        consts = {}
        for type, enum in node.children():
            consts[enum.name] = value = resolve_ast(enum.value, consts)
            enum.value = c_ast.Constant('int', str(value))
    return ast

def resolve_ast(ast, consts):
    if isinstance(ast, c_ast.Constant):
        return int(ast.value)
    elif isinstance(ast, c_ast.ID):
        return consts[ast.name]
    elif isinstance(ast, c_ast.BinaryOp):
        return resolve_ast(ast.left, consts) | resolve_ast(ast.right, consts)
    else:
        raise RuntimeError('Unexpected ast node: %r' % ast)


ffi = FFI()
ffi.cdef(get_cdef())
ffi.cdef('''
extern "Python" {
    static bool pycall_parser_new_struct(TCOD_parser_struct_t str,const char *name);
    static bool pycall_parser_new_flag(const char *name);
    static bool pycall_parser_new_property(const char *propname, TCOD_value_type_t type, TCOD_value_t value);
    static bool pycall_parser_end_struct(TCOD_parser_struct_t str, const char *name);
    static void pycall_parser_error(const char *msg);

    static bool _pycall_bsp_callback(TCOD_bsp_t *node, void *userData);

    static float _pycall_path_func( int xFrom, int yFrom, int xTo, int yTo, void *user_data );

    static bool _pycall_line_listener(int x, int y);

    static void _pycall_sdl_hook(void *);
}
''')
#with open('src/libtcod_cdef.h', 'r') as file_cdef:
#    ffi.cdef(file_cdef.read())
ffi.set_source(
    module_name, source,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    sources=sources,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    define_macros=define_macros,
)

if __name__ == "__main__":
    ffi.compile()
