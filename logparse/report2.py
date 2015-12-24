#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================
#
# Filename:	report.py
#
# Author:		Oxnz
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
# Copyright (c) 2015 Oxnz
#
# Distributed under terms of the [LICENSE] license.
# [license]
#
# ===============================================================
#

import sys
import time
import operator

import FastInt

class Task(object):
    def __init__(self, lines):
        super(Task, self).__init__()
        self._lines = lines
        self._NL = 0
        self._TMQ = [0] * 52
        self._TT = 0
        self._QSPN = 0

    @property
    def lines(self):
        return self._lines

    @property
    def NL(self):
        return self._NL

    @property
    def TMQ(self):
        return self._TMQ

    @property
    def TT(self):
        return self._TT

    @property
    def QSPN(self):
        return self._QSPN

    @property
    def timecost(self):
        return self._timecost

    def accumulate(self, line):
        self._NL += 1
        prefix = 'tm=('
        suffix = ')'
        a = line.find(prefix)
        b = line.find(suffix, a)
        if a == -1 or b == -1:
            print 'malformed line: [{}]'.format(line.rstrip())
            return
        vals = line[a + len(prefix) : b]
        sep = '|'
        vals = vals.split(sep)
        vals = map(FastInt.fastInt, vals)
        self._TMQ = map(operator.add, self._TMQ, vals)
        prefix = 'tt='
        suffix = ' '
        a = line.find(prefix, b)
        b = line.find(suffix, a)
        if a == -1 or b == -1:
            print 'malformed line: [{}]'.format(line.rstrip())
            return
        self._TT += int(line[a + len(prefix) : b])
        prefix = 'qspn='
        suffix = ' '
        a = line.find(prefix, b)
        b = line.find(suffix, a)
        if a == -1 or b == -1:
            print 'malformed line: [{}]'.format(line.rstrip())
            return
        self._QSPN += int(line[a + len(prefix) : b])

    def run(self):
        print '{} begin, nline = {}'.format(self, len(self._lines))
        ts0 = time.clock()
        for line in self._lines:
            self.accumulate(line)
        ts1 = time.clock()
        self._timecost = ts1 - ts0
        print '{} end'.format(self)

def parse(lines):
    print 'parse begin'
    task = Task(lines)
    task.run()
    report([task])

def report(taskq):
    NL = 0
    TMQ = [0] * 52
    TT = 0
    QSPN = 0
    for task in taskq:
        NL += task.NL
        TMQ = map(operator.add, TMQ, task.TMQ)
        TT += task.TT
        QSPN += task.QSPN
    print '''
----------------------------report----------------------------
NL: {}
TMQ({})
TT:{}
QSPN: {}
============================report============================
    '''.format(NL, TMQ, TT, QSPN)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        fname = 'bj.log'
    with open(fname) as file_:
        parse(file_.readlines())
