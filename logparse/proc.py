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

import sys
import time
import pprint
import operator
import threading
import multiprocessing as mp

import FastInt

def timecost(func):
    '''benchmark func'''
    def decorator(*args, **kwargs):
        ts0 = time.clock()
        result = func(*args, **kwargs)
        ts1 = time.clock()
        timediff = ts1 - ts0
        print 'time cost: {0}'.format(timediff)
        return result

    return decorator

class Task(mp.Process):
    def __init__(self, lino, lines):
        super(Task, self).__init__()
        self._lines = lines
        self._NL = lino
        self._TMQ = [0] * 52
        self._TT = 0
        self._QSPN = 0
        self._exp = Exception('prefix or suffix not found')

    @property
    def count(self):
        return {
                'nline':self._NL,
                'tm':   self._TMQ,
                'tt':   self._TT,
                'qspn': self._QSPN,
                }

    def accumulate(self, line):
        try:
            self._NL += 1
            prefix = 'tm=('
            suffix = ')'
            b = 100
            a = line.find(prefix, b)
            b = line.find(suffix, a)
            if a == -1 or b == -1:
                raise self._exp
            #vals = line[a + len(prefix) : b]
            vals = line[a + 4 : b]
            sep = '|'
            vals = vals.split(sep)
            vals = map(FastInt.toInt, vals)
            self._TMQ = map(operator.add, self._TMQ, vals)
            prefix = 'tt='
            suffix = ' '
            a = line.find(prefix, b)
            b = line.find(suffix, a)
            if a == -1 or b == -1:
                raise self._exp
            #self._TT += FastInt.toInt(line[a + len(prefix) : b])
            self._TT += FastInt.toInt(line[a + 3 : b])
            prefix = 'qspn='
            suffix = ' '
            a = line.find(prefix, b)
            b = line.find(suffix, a)
            if a == -1 or b == -1:
                raise self._exp
            #self._QSPN += FastInt.toInt(line[a + len(prefix) : b])
            self._QSPN += FastInt.toInt(line[a + 5 : b])
        except Exception as e:
            print >> sys.stderr, '*** malformed line {0}: {1}'.format(self._NL, e)

    def run(self):
        map(self.accumulate, self._lines)

# 2S = a1 + an
# 2S = a1 + a1 + (n-1)d
# 2S = 2a1 + (n-1)d
# 2S = 2a1 + (n-1)pa1
# 2S = a1(2 + (n-1)p)
# a1 = 2S/n(2 + (n-1)p)
def ranges(s, n, p):
    if p < 0 or p > 1:
        raise Exception('invalid percent')
    if n > s:
        raise Exception('invalid s or n')
    a1 = 2*s/(n*(2 + (n-1)*p))
    d = p * a1
    start = 0
    for i in range(n):
        ai = a1 + i * d
        step = ai
        end = start + step
        yield (int(start), int(end))
        start = end

def parse(lines, nproc):
    nline = len(lines)
    step = (nline + nproc - 1) / nproc
    delta = 0.01
    for a, b in ranges(nline, nproc, delta):
        print '(lines[{}:{}])'.format(a, b)
    taskq = [Task(a, lines[a:b]) for a, b in ranges(nline, nproc, 0.01)]
    #taskq = [Task(i, lines[i:i+step]) for i in range(0, nline, step)]
    for task in reversed(taskq):
        print '+ {0}'.format(task)
        task.start()
    for task in taskq:
        task.join()
        print '- {0}'.format(task)
    report(taskq)

def count(stat1, stat2):
    for key in ('tt', 'qspn'):
        stat1[key] += stat2[key]
    for key in ('tm'):
        stat1['tm'] = map(operator.add, stat1['tm'], stat2['tm'])
    return stat1

def report(taskq):
    statq = (task.count for task in taskq)
    stat = reduce(count, statq, {
        'tm':   [0] * 52,
        'tt':   0,
        'qspn': 0,
        })
    print '----------------------------report----------------------------'
    pprint.pprint(stat)
    print '=============================================================='

from getopt import (getopt, GetoptError)

def help(name):
    print 'Usage: {0} <logfile>...'.format(name)

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
    if len(args) == 0:
        help(sys.argv[0])
        sys.exit(1)
    lines = []
    for fpath in args:
        with open(fpath) as f:
            lines += f.readlines()
    parse(lines, nproc)
