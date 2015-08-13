#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author: zhangpan05

'''find no parent page(s)'''

import os
import glob
import urllib
import sys
import subprocess
import time
import re
import string

class DumpOutput(object):
    '''duplicate stdout to file handle'''
    def __init__(self, dupf):
        self.dup = dupf
        self.out = sys.stdout

    def __enter__(self):
        sys.stdout = self

    def write(self, line):
        self.dup.write(line)
        self.out.write(line)

    def __exit__(self, type_, value, traceback):
        sys.stdout = self.out
        return False

    def __del__(self):
        pass

def staticvariable(name, val):
    '''
Convert a variable to be a static variable.

To declare a static variable, use this idiom:

    @staticvariable('var_name', 'var_value')
    def foo():
        print foo.var_name

    '''

    def decorate(func):
        setattr(func, name, val)
        return func
    return decorate

def ptimestamp(func):
    '''print timestamp before and after the func call'''
    def decorate(*args, **kwargs):
        print time.strftime('%F %T'), func.__name__, 'begin'
        result = func(*args, **kwargs)
        print time.strftime('%F %T'), func.__name__, 'done'
        return result
    return decorate

# wpth: working path
# oname: orignal name
@staticvariable('fltcnt', 0)
def needname(wpth, oname):
    '''test if exists file corresponding to a malformed file name'''
    if oname in ('WebChanges.txt', 'WebSearch.txt', 'WebTopicList.txt',
        'WebNotify.txt', 'WebPreferences.txt', 'WebRss.txt'):
        needname.fltcnt += 1
        return False
    try:
        tname = oname.decode('utf-8').encode('latin1')
        if oname != tname and os.path.exists(os.path.join(wpth, tname)):
            needname.fltcnt += 1
            return False
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    return True

# plpf: parent loop file
# fn: file name
# pl: parent line
@staticvariable('pdct', {})
@staticvariable('pntr', re.compile('%META:TOPICPARENT{name="(.*)"}%'))
@staticvariable('plpcnt', 0)
def chkprnt(plpf, fn, pl):
    '''check if parent loops'''
    m = chkprnt.pntr.match(pl)
    if m:
        parent = m.groups()[0]
        if chkprnt.pdct.has_key(fn):
            raise Exception('{} has more than one parent: {}, {}' \
                .format(fn, chkprnt.pdct[fn], parent))
        chkprnt.pdct[fn] = parent
        p = parent
        plst = [fn, p]
        ps = set(plst)
        while chkprnt.pdct.has_key(p):
            p = chkprnt.pdct[p]
            plst.append(p)
            if p in ps:
                print >>plpf, '->'.join(plst)
                chkprnt.plpcnt += 1
                break
            else:
                ps.add(p)

# link candidate formats:
#    [/twiki/bin/view/path/to/fname(#|?|])
#    [http(s)://twiki/bin/view/path/to/fname(#|?|])
#    <a href="(http(s)://twiki/bin/view/path/to/fname(#|?|"| |)
#    [fname]
def linkto(fc, fn):
    '''check if fc contains link linked to fn'''
    fcl = len(fc)
    fnl = len(fn)
    i = 0
    while True:
        j = fc.find(fn, i)
        if -1 == j or j+fnl == fcl:
            return False
        elif 0 == j:
            i = j + fnl
            continue
        if fc[j-1] == '[' and fc[j+fnl] == ']': #[fname]
            return True
        if not fc[j-1] in ('/', '.'):
            i = j + fnl
            continue
        la = fc.rfind('<a', i, j)
        lb = fc.rfind('[', i, j)
        if -1 == la and -1 == lb:
            i = j + fnl
            continue
        elif la < lb and fc[j+fnl] in ('#', '?', ']'):
            return fc[j-1] == '.' or lb == max(
                fc.rfind('[/twiki/bin/view/', i, j),
                fc.rfind('[http://twiki/bin/view/', i, j),
                fc.rfind('[https://twiki/bin/view/', i, j),
                fc.rfind('[http://wiki.babel.baidu.com/twiki/bin/view/', i, j)
            )
        elif lb < la and fc[j+fnl] in ('#', '?', '"', ' '):
            return fc[j-1] == '.' or la < max(
                fc.rfind('"http://twiki/bin/view/', i, j),
                fc.rfind('"https://twiki/bin/view/', i, j),
                fc.rfind('"http://wiki.babel.baidu.com/twiki/bin/view/', i, j)
            )
        else:
            i = j + fnl
            continue
    return False


def genditem(fname):
    oname = fname
    fname = os.path.splitext(fname)[0]
    return oname, [[fname, urllib.quote(fname)], set()]

# INPUT:
# wpth: working path
# pnfname: no parent file list file
@staticvariable('pnfcnt', 0)
@ptimestamp
def process(erpf, wpth, pnfname, plpfname):
    with open(pnfname, 'r') as f:
        rdict = dict(genditem(fname) for fname in \
            (line.rstrip() for line in f) if needname(wpth, fname))
        process.pnfcnt = len(rdict)

    print 'processing pattern [{}]'.format(os.path.join(wpth, '*.txt'))
    with open(plpfname, 'w') as plpf:
        for fname in glob.glob(os.path.join(wpth, '*.txt')):
            print fname
            with open(fname, 'r') as f:
                fname = os.path.splitext(os.path.basename(fname))[0]
                f.readline() # skip first line
                chkprnt(plpf, fname, f.readline().rstrip())
                fc = f.read()
                for key in rdict:
                    for fn in rdict[key][0]:
                        if linkto(fc, fn) and \
                            os.path.splitext(key)[0] != fname:
                            rdict[key][1].add(fname)
    return rdict

def getcma(fpth):
    '''get create time, last-modified time and author from version file'''
    file_ = fpth + ',v'
    if not os.path.exists(file_):
        print '{} not exists'.format(file_)
        # no version file, use self cmtime instead
        return os.path.getctime(fpth), os.path.getmtime(fpth), 'TWikiGuest'
    cmd = \
        r'/^1.1$/{N;s/1.1\ndate\t\(.*\);\tauthor \(.*\);\tstate.*$/\1:\2/;p;q}'
    p = subprocess.Popen(['sed', '-ne', cmd, file_], stdout=subprocess.PIPE)
    o, e = p.communicate()
    if e:
        ct, au = os.path.getctime(file_), 'TWikiGuest'
    else:
        ct, au = o.rstrip().split(':')
        ct = time.mktime(time.strptime(ct, '%Y.%m.%d.%H.%M.%S'))
    mt = os.path.getmtime(file_)
    return ct, mt, au

def fmtime(t):
    '''format secs to str'''
    fmt = '%F %T'
    return time.strftime(fmt, time.localtime(t))

# INPUT:
# wpth: working path
# rdict: result dict with file -> [parent list] pairs
# OUTPUT:
# lnf: link not found file
# rsbf: resolvable file list, aka, only 1 link found
# urbf: unresolvable file list, aka, multiple links found
@staticvariable('lnfcnt', 0)
@staticvariable('rsbcnt', 0)
@staticvariable('urbcnt', 0)
@ptimestamp
def report(wpth, rdict, lnf, rsbf, urbf):
    '''generate report based on rdict'''
    for key in rdict:
        pset = rdict[key][1]
        cnt = len(pset)
        if 0 == cnt:
            report.lnfcnt += 1
            mt = os.path.getmtime(os.path.join(wpth, key))
            print >>lnf, '[{}]\n{}->{}'.format(fmtime(mt),
                os.path.join(wpth, key), 'WebHome')
        elif 1 == cnt:
            report.rsbcnt += 1
            print >>rsbf, '{0}->{1}'.format(os.path.join(wpth, key),
                pset.pop())
        else:
            report.urbcnt += 1
            pct, mt, au = getcma(os.path.join(wpth, key))
            print >>urbf, '{}->\n    meta:{}, {}, {}'.format(os.path.join(wpth, key), au, fmtime(pct),
                fmtime(mt))
            # before, after set
            pb, pa = set(), set()
            for p in pset:
                ct, mt, au = getcma(os.path.join(wpth, p + '.txt'))
                if ct < pct:
                    pb.add('\t[{}, {}, {}, {}]'.format(p, au, fmtime(ct),
                        fmtime(mt)))
                else:
                    pa.add('\t[{}, {}, {}, {}]'.format(p, au, fmtime(ct),
                        fmtime(mt)))
            if len(pb):
                print >>urbf, '    before:'
                print >>urbf, '\n'.join(pb)
            if len(pa):
                print >>urbf, '    after:'
                print >>urbf, '\n'.join(pa)
    suminfo = summary(process.pnfcnt,
        report.lnfcnt,
        chkprnt.plpcnt,
        report.rsbcnt,
        report.urbcnt,
        needname.fltcnt)
    print suminfo

def summary(pnfcnt, lnfcnt, plpcnt, rsbcnt, urbcnt, fltcnt):
    '''generate log items'''
    return '''{} Summary Info {}
{} parentNotFound
{} duplicated
{} linkNotFound
{} parentLoop
{} resolvable
{} unresolvable.out
parentNotFound - duplicated = {}
linkNotFound + resolvable + unresolvable = {}
{}
'''.format('-'*30, '-'*30,
    pnfcnt,
    fltcnt,
    lnfcnt,
    plpcnt,
    rsbcnt,
    urbcnt,
    pnfcnt -  fltcnt,
    lnfcnt + rsbcnt + urbcnt,
    '='*80)


# INPUT:
# wpth: working path
# scpt: shell script
# OUTPUT:
# pnfname: parent not found file
@ptimestamp
def prefix(erpf, wpth, scpt, pnfname):
    '''call the prefix.sh to generate parent not found file'''
    with open(pnfname, 'w') as pnf:
        subprocess.call([scpt, wpth], stdout=pnf, stderr=erpf)

@ptimestamp
def main(wpth, lnpscpt, pfxscpt):
    bpth = os.path.basename(wpth)
    if 0 == len(bpth):
        raise Exception("bad path argument")
    if os.path.exists(bpth):
        raise Exception("file or directory already exists: " + bpth)
    else:
        os.mkdir(bpth)
    pnfname = os.path.join(bpth, 'parentNotFound.out')
    lnfname = os.path.join(bpth, 'linkNotFound.out')
    rsbfname = os.path.join(bpth, 'resolvable.out')
    urbfname = os.path.join(bpth, 'unresolvable.out')
    erpfname = os.path.join(bpth, 'errorReport.out')
    plpfname = os.path.join(bpth, 'parentLoop.out')
    logfname = os.path.join(bpth, 'process.log')

    with open(logfname, 'w') as logf, open(erpfname, 'w') as erpf, DumpOutput(logf):
        prefix(erpf, wpth, lnpscpt, pnfname)
        with open(lnfname, 'w') as lnf, open(rsbfname, 'w') as rsbf, \
            open(urbfname, 'w') as urbf:
            rdct = process(erpf, wpth, pnfname, plpfname)
            report(wpth, rdct, lnf, rsbf, urbf)
        #postfix(logf, erpf, pfxscpt, rsbfname)

# fix parent missing
@ptimestamp
def postfix(logf, erpf, scpt, rsbfname):
    subprocess.call([scpt, rsbfname], stdout=logf, stderr=erpf)

# INPUT:
#   lnfs: link not found file set
def postchk(wpth, lnfns, lnf):
    print >>lnf, '---------------------post checking-------------------------'
    alnums = string.digits + string.ascii_letters
    for lnfn in lnfns:
        lnfnl = len(lnfn)
        for fname in glob.glob(os.path.join(wpth, '*.txt')):
            with open(fname) as f:
                f.readline()
                f.readline()
                fc = f.read()
                fcl = len(fc)
                i = 0
                while -1 != i:
                    if i+lnfnl < fcl and not fc[i+lnfnl] in alnums:
                        print '{} found for {} in {}'.format(fc[i:i+lnfnl+1],
                            lnfn, fname)
                        print >>lnf, '{} found for {} in {}' \
                            .format(fc[i:i+lnfnl+1], lnfn, fname)
                    i = fc.find(lnfn, i+lnfnl)

if __name__ == '__main__':
    if 4 == len(sys.argv):
        wpth = os.path.abspath(sys.argv[1])
        lnpscpt = os.path.abspath(sys.argv[2])
        pfxscpt = os.path.abspath(sys.argv[3])
        main(wpth, lnpscpt, pfxscpt)
    else:
        print 'Usage: {0} path list-no-parent-script fix-no-parent-script' \
            .format(sys.argv[0])
        sys.exit(1)

# vim: ts=4 et sw=4
