#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================
#
# Filename:	parse.py
#
# Author:		Oxnz
# Email:		yunxinyi@gmail.com
# Created:		2016-09-02 11:11:14 CST
# Last-update:	2016-09-02 11:11:14 CST
# Description: ANCHOR
#
# Version:		0.0.1
# Revision:	[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# License:
# Copyright (c) 2016 Oxnz
#
# Distributed under terms of the [LICENSE] license.
# [license]
#
# ===============================================================
#

import sys
import re

if len(sys.argv) < 2:
    print('p <file>')
    sys.exit(1)
pat = re.compile('[^ ]* - - \[[^]]*\] "[^ ]* [^?]*(\?[^ ]*)?')
f = open(sys.argv[1])
for line in f:
    line = '10.44.64.22 - - [09/Mar/2016:00:02:22 +0800] "GET /alfresco/s/api/sites/issue-BPIT/memberships/xn_monitor01?alf_ticket=TICKET_0d07f2c12253a532b0cee69e787d6ddc3ecce2cc HTTP/1.1" 404 385 "-" "Jakarta Commons-HttpClient/3.1" 14 0.014 TP-Processor58'
    (ip, _, _, ts, tz, method, url, ver, status, size, _, _, agent, sec, ms, tid) = line.split(' ')
    if re.match(line):
        print 'match'
    else:
        print 'not match'
