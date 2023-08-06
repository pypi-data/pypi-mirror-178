from __future__ import annotations

import glob
import os
from os.path import join as jpath
from ctypes import CDLL

import numpy as np
import distutils.ccompiler

_lib_ext = distutils.ccompiler.new_compiler().shared_lib_extension

echaimlib_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "source_c/cmake-build-debug"
)

# echaimlib_path = os.path.dirname(os.path.abspath(__file__))


def _import_libs():
    echaimlib = CDLL(jpath(echaimlib_path, "libECHAIM"+_lib_ext))
    return echaimlib


def _move_libs():
    parent_dir = os.path.abspath(jpath(echaimlib_path, '..'))
    libs = glob.glob(jpath(parent_dir, 'libECHAIM*'))
    for lib in libs:
        parent, file = os.path.split(lib)
        os.rename(lib, jpath(parent, 'echaim', file))


try:
    echaimlib = _import_libs()
except OSError:
    _move_libs()
    try:
        echaimlib = _import_libs()
    except OSError:
        raise ImportError("Could not import E-CHAIM libraries. Please make sure you have installed the package "
                          "correctly.")
