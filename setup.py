#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
This file is part of PyHunspell.

PyHunspell is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyHunspell is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyHunspell. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import platform
import re
from distutils.core import setup, Extension
from distutils.sysconfig import get_config_var

main_module_kwargs = {"sources": ['hunspell.c']}
if platform.system() == "Windows":
    main_module_kwargs['macros'] = [('HUNSPELL_STATIC', None)]
    main_module_kwargs['libraries'] = ['libhunspell']
    main_module_kwargs['include_dirs'] = ['V:/hunspell-1.3.3/src/hunspell']
    main_module_kwargs['library_dirs'] = ['V:/hunspell-1.3.3/src/win_api/x64/Release/libhunspell']
    main_module_kwargs['compile_args'] = ['/MT']
else:
    all_probable_libs = []
    lib_presence = re.compile(r"^libhunspell[-.](\d+\.?)*\.so[0-9.]*$")
    for dirname, _, lib_names in os.walk(get_config_var("LIBDIR")):
        if "libhunspell.so" in lib_names:
            print("%s %s" % (dirname, lib_names))
            print([l for l in lib_names
                   if not os.path.islink(os.path.join(dirname, l))])
            print([l for l in lib_names
                   if lib_presence.match(l)])
            print([l for l in lib_names
                   if not os.path.islink(os.path.join(dirname, l))
                   and lib_presence.match(l)])
        all_probable_libs.extend([l for l in lib_names
                                  if not os.path.islink(os.path.join(dirname, l))
                                  and lib_presence.match(l)])
    try:
        lib = all_probable_libs.pop()
    except IndexError:
        exit('libhunspell.so or similar not found. '
             'Please install hunspell-dev package. '
             'If it is installed feel free to report '
             'a bug here: https://github.com/blatinier/pyhunspell/issues')
    main_module_kwargs['macros'] = [('_LINUX', None)]
    main_module_kwargs['libraries'] = ['hunspell']
    main_module_kwargs['include_dirs'] = '/usr/include/hunspell',
    main_module_kwargs['compile_args'] = ['-Wall']

main = Extension('hunspell', **main_module_kwargs)

setup(name="hunspell",
      version="0.4.2",
      description="Module for the Hunspell spellchecker engine",
      author="Benoît Latinier",
      author_email="benoit@latinier.fr",
      url="http://github.com/blatinier/pyhunspell",
      ext_modules=[main],
      license="LGPLv3",
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'License :: OSI Approved'
          ' :: GNU Lesser General Public License v3 (LGPLv3)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing :: Linguistic',
      ])
