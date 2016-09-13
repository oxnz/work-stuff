#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================
#
# Filename:	trans.py
#
# Author:		oxnz
# Created:		2016-05-13 16:06:59 CST
# Last-update:	2016-05-13 16:06:59 CST
#
# Version:		0.0.1
# Revision:	[None]
# Revision history:	[None]
# Date Author Remarks:	[None]
#
# ===============================================================

import time
import requests
import mysql.connector

repoServer = 'http://xx.xx.x.xx:80/alfresco'
onlineEditServer = 'http://xx.xx.x.xxx'
repoU = 'username'
repoP = 'password'
auth = (repoU, repoP)
headers = {'From': 'xxx'}
config = {
    'host': 'xx.xx.xx.xx',
    'port': 3307,
    'user': 'username',
    'password': 'pass',
    'database': 'dbname'
}

def proc():
    url = '{0}/api/file/editedCodes'.format(onlineEditServer)
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        raise RuntimeError('[{0}] versions status code == {1}'.format(code, r.status_code))
    data = r.json()['data']
    data = ['dddddddd-5438-4c6d-b2bb-3aa31a44a837']
    for code in data:
        trans(code)
        delURL = '{0}/api/file/{1}'.format(onlineEditServer, code)
        requests.delete(delURL, headers = headers)
        print '[{0}] : success'.format(code)

def trans(code):
    vurl = '{0}/api/file/{1}/versions'.format(onlineEditServer, code)
    r = requests.get(vurl, headers = headers)
    if r.status_code != 200:
        raise RuntimeError('[{0}] versions status code == {1}'.format(code, r.status_code))
    data = r.json()
    msg = data['message']
    if msg != None and msg.startswith('file not exists'):
        print('{0} not exists'.format(code))
        return
    vers = data['data']
    majorVer = 'true'
    for ver in vers:
        print('[{0}] vno: {1} user: {2} url: [{3}]'.format(ver['time'], ver['vno'], ver['user'], ver['url']))
        durl = '{0}/api/file/{1}/v/{2}'.format(onlineEditServer, code, ver['vno'])
        r = requests.get(durl, headers = headers)
        if r.status_code != 200:
            raise RuntimeError('[{0}] download status code == {1}'.format(code, r.status_code))
        fname = '{0}-{1}'.format(code, ver['vno'])
        with open(fname, 'w') as f:
            f.write(r.content)
        mtime = long(1000*time.mktime(time.strptime(ver['time'], '%Y-%m-%d %H:%M:%S')))
        post(code, fname, majorVer, ver['user'], mtime)
        # TODO: delete fname
        majorVer = 'false'

def post(code, fpath, majorVer, user, mtime):
    print('upload {0}'.format(fpath))
    nodeURL = '{0}/s/api/storepath/workspace/SpacesStore/{1}'.format(repoServer, code)
    r = requests.get(nodeURL)
    if r.status_code != 200:
        raise RuntimeError('[{0}] get node info failed with code = {1}'.format(code, r.status_code))
    resp = r.json()
    siteID = resp['site']
    path = resp['filePathInAlfresco']
    if path.endswith('documentLibrary/'):
        path = '/'
    else:
        path = path.split('documentLibrary')[1]
    nodeRef = 'workspace://SpacesStore/{0}'.format(code)
    desc = '[creator-start]{0}[creator-end][modifyTime-start]{1}[modifyTime-end]'.format(user, mtime)
    params = {
            'siteId':siteID,
            'containerId':'documentLibrary',
            'overwrite':'true',
            'updateNodeRef':nodeRef,
            'majorVersion':majorVer,
            'Upload':'Submit Query',
            'UploadDirectory':path,
            'description': desc,
            }
    #files = {'filedata':(fpath, open(fpath, 'rb'), 'application/octec-stream')}
    files = {'filedata':(fpath, open(fpath, 'rb'))}
    url = '{0}/s/api/upload'.format(repoServer)
    resp = requests.post(url, data=params, files=files, auth = auth)
    if resp.status_code != 200:
        raise RuntimeError('[{0}] update failed'.format(code))
    # update meta info
    mtime = time.strftime('%FT%T.000+08:00', time.gmtime(mtime/1000.0))
    update(code, user, mtime)

def update(uuid, user, mtime):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    stmt = 'update alf_node set audit_modifier = "{0}", audit_modified = "{1}" where uuid = "{2}";'.format(user, mtime, uuid)
    print 'exec:', stmt
    cursor.execute(stmt)
    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    #proc()
    delete()
