#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================
#
# Filename:	setup.py
#
# Author:		Oxnz
# Email:		yunxinyi@gmail.com
# Created:		2015-12-28 09:46:31 CST
# Last-update:	2015-12-28 09:46:31 CST
# Description: ANCHOR
#
# Version:		0.0.1
# Revision:	[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# License:
# Copyright (c) 2015 Oxnz
#
# Distributed under terms of the [LICENSE] license.
# [license]
#
# ===============================================================
#

from distutils.core import setup
from distutils.extension import Extension

__version__ = '0.1'

FastInt = Extension(
        'FastInt',
        sources = ['FastInt/FastInt.c'],
        extra_compile_args = ['-O3', '-std=c99', '-Wall'],
        extra_link_args = [],
        )

setup(
        name = __name__,
        version = __version__,
        ext_modules = [FastInt],
        )
