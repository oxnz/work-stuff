#!/usr/bin/env python
# -*- coding: utf-8 -*-
# elasticsearch rankdiff

import requests
import itertools

def search(es, index, q, Q):
    print es, q, index, 'http://{}/{}/_search'.format(es, index)
    resp = requests.post('http://{}/{}/_search'.format(es, index),
            headers = {'content-type': 'application/json'},
            auth = ('user', 'pass'),
            data = open(q).read().replace('Q', Q))
    return resp.json()

def echo(a, b):
    return '{} : {}'.format(
            a['_source']['title'].encode('utf-8'), b['_source']['title'].encode('utf-8'))

def rdiff(a, b):
    print 'A (orig) B (new)\nhits: {} {}'.format(a['hits']['total'], b['hits']['total'])
    i=0
    for e in itertools.imap(echo, a['hits']['hits'], b['hits']['hits']):
        i+=1
        print '{}: {}'.format(i, e)

def main(es, q1, q2, index, Q):
    rdiff(search(es, index, q1, Q), search(es, index, q2, Q))

if __name__ == '__main__':
    Q = '青云志2'
    Q = '李易峰心理罪'
    Q = '极限特工'
    main('100.200.3.4:8080', 'q1', 'q2', 'media_search', Q)
