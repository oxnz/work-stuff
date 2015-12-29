#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================
#
# Filename:	report.py
#
# Author:		zhangpan
# Email:		yunxinyi@gmail.com
# Created:		2015-12-23 13:53:10 CST
# Last-update:	2015-12-23 13:53:10 CST
# Description: ANCHOR
#
# Version:		0.0.1
# Revision:	[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# License:
# Copyright (c) 2015 zhangpan. All rights reserved.
#
# ===============================================================
#

import os
import re
import sys
import time
import pprint
import operator
import functools
import threading

import FastInt

import numpy as np
import multiprocessing as mp

def timefunc(func):
    '''benchmark func'''
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        ts0 = time.clock()
        tm0 = time.time()
        result = func(*args, **kwargs)
        ts1 = time.clock()
        tm1 = time.time()
        tsdiff = ts1 - ts0
        tmdiff = tm1 - tm0
        print 'time cost of {2}: {0} {1}'.format(tmdiff, tsdiff, func.func_name)
        return result
    return decorator

#NOTICE: 12-21 00:00:00:  imas * 26706 [ÄÚÒÂµê] qry=ÄÚÒÂµê ip=223.98.252.57 rt_ip=10.128.205.21 pn=0 tn= pre=0 s=327126f4b415f974 bd=AD4890C25E3E24A41E13CF3FE2BACB44 cuid=E382D676F6FFB6674CAC94DF6C8DECD9|789195320493468 imei= idm=(2,2,0) src=915, fn=cnkang_cpr tm=(128|11447|16998|8770|0|0|0|0|0|0|0|0|0|0|0|0|15728|0|179|16421|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|9307|0|0|0|0|0|0|0|0|0|0|0|0) tt=79203 sp=(51985,8388608) inner=1 ft=37 ppq=0 csfn=(6|9) bsrn=(47|47,) amrn=47 qspn=2 ws=1 di=1(47/47|47) qs_kpi=(0|2|0) it=(0|15480|11339|16111|0|0|15152|0|0|7909|0|0|0|0|0) mem=(5)([18168263][0][0][0][0] 32M[0]) pack=333414 tmo=0 qs_cmd_time=() extra_log=fetch:9,before_write:69852,fengsui:1,all_except_conn:79216, 
class Task(mp.Process):
    pattern = re.compile(r'tm=\(([^)]+)\) tt=(\d+).*qspn=(\d+)')
    def __init__(self, lines):
        super(Task, self).__init__()
        self._lines = lines
        self._NR = 0
        self._ST = [0] * 54

    @property
    def nrecord(self):
        return self._NR

    @property
    def stat(self):
        return self._ST

    def run(self):
        for line in self._lines:
            try:
                m = Task.pattern.search(line)
                #FastInt.add(self._CNT, '|'.join(m.groups()))
                self._ST = map(operator.add, self._ST,
                        map(FastInt.toInt, ('|'.join(m.groups())).split('|')))
                self._NR += 1
            except Exception as e:
                print >> sys.stderr, '*** malformed line {0}'.format(e)

@timefunc
def parse(lines, nproc):
    nline = len(lines)
    step = (nline + nproc - 1)/nproc
    taskq = map(Task, [lines[i:i+step] for i in range(0, nline, step)])
    for task in taskq:
        task.start()
        print '+ {0}'.format(task)
    for task in taskq:
        task.join()
        print '- {0}'.format(task)
    statq = [task.stat for task in taskq]
    stat = reduce(operator.add, map(np.array, statq))
    print 'report'.center(80, '-')
    print stat
    print ''.center(80, '=')

from getopt import (getopt, GetoptError)

def help(name):
    print 'Usage: {0} <logfile>'.format(name)

if __name__ == '__main__':
    try:
        opts, args = getopt(sys.argv[1:], 'hn:', ['help', 'nproc'])
    except GetoptError as e:
        print e
        sys.exit(1)
    nproc = mp.cpu_count()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help(sys.argv[0])
            sys.exit(0)
        elif opt in ('-n', '--nproc'):
            nproc = int(arg)
        else:
            print >> sys.stderr, 'invalid opt: {0}'.format(opt)
            sys.exit(1)
    nargs = len(args)
    if nargs == 0 or nargs > 1:
        help(sys.argv[0])
        sys.exit(1)
    fpath = args[0]
    with open(fpath) as f:
        parse(f.readlines(), nproc)
