#!/usr/local/bin/python
#coding:utf-8
__author__ = 'mUSicX'

import os, re, codecs

code_regex = re.compile(r"[a-zA-Z0-9]{2,5}-?\d{2,5}")
good = 'J:\\AV\\names'
bad = 'J:\\AV\\nonames'

if __name__ == '__main__':
    out = open('walk.txt', 'w')
    for root, dirs, files in os.walk('J:\\AdultVideo'):
        for file_name in files:
            out.write('{}\\{}\n'.format(root, file_name))

