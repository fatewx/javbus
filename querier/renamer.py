#!/usr/local/bin/python
#coding:utf-8
__author__ = 'mUSicX'

import os, re, codecs

code_regex = re.compile(r"[a-zA-Z0-9]{2,5}-?\d{2,5}")
good = u'J:\\AV\\names'
bad = u'J:\\AV\\nonames'

if __name__ == '__main__':
    lines = codecs.open('database.txt', encoding='utf-8').readlines()
    full_names = [x.split('|') for x in lines]
    valid_names = [(x[0].lower().replace('-',''), x[1]) for x in full_names]
    names = dict([x for x in valid_names if x[1] != '' and len(x[1].split(',')) < 3])
    nonames = dict([x for x in valid_names if x[1] == '' or len(x[1].split(',')) >= 3])
    out = codecs.open('error.txt', 'w', encoding='utf-8')
    for root, dirs, files in os.walk('J:\\AdultVideo'):
        for file in files:
            upath = root.decode('gbk') + u'\\' + file.decode('gbk')
            match = code_regex.search(file)
            if match:
                code = match.group()
                key = code.replace('-','').lower()
                if key in names:
                    name = names[key]
                    out.write(u'rename "{}" "{}"\n'.format(upath, good + u'\\' + file.replace(code, '{} -[{}]'.format(name, key).encode('gbk'))))
                elif key in nonames:
                    out.write(u'rename "{}" "{}"\n'.format(upath, bad + u'\\' + file.decode('gbk')))
                else:
                    out.write(u'# don\'t touch {}\n'.format(upath))
            else:
                out.write(u'# cannot match {}\n'.format(upath))
