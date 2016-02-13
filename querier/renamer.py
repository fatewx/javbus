#!/usr/local/bin/python
#coding:utf-8
__author__ = 'mUSicX'

import os, re, codecs

code_regex = re.compile(r"[a-zA-Z0-9]{2,5}-?\d{2,5}")
good = u'I:\\AV\\Named'
bad = u'I:\\AV\\Mixed'

if __name__ == '__main__':
    lines = codecs.open('database.txt', encoding='utf-8').readlines()
    full_names = [x.split('|') for x in lines]
    valid_names = [(x[0].lower().replace('-',''), (x[0],x[1],x[2])) for x in full_names]
    names = dict([x for x in valid_names if x[1][1] != '' and len(x[1][1].split(',')) < 3])
    nonames = dict([x for x in valid_names if x[1][1] == '' or len(x[1][1].split(',')) >= 3])
    out = codecs.open('rename.txt', 'w', encoding='utf-8')
    for root, dirs, files in os.walk('I:\\AV\\abc'):
        for file in files:
            upath = root.decode('gbk') + u'\\' + file.decode('gbk')
            match = code_regex.search(file)
            if match:
                code = match.group()
                key = code.replace('-','').lower()
                if key in names:
                    number, name, title = names[key]
                    file_replace = file.replace(code, u'{} - [{}]'.format(name, number))
                    out.write(u'move "{}" "{}"\n'.format(upath, good + u'\\' + file_replace))
                elif key in nonames:
                    number, name, title = nonames[key]
                    memo = name if name != '' else title
                    file_replace = file.replace(code, u'[{}] - {}'.format(number, memo))
                    out.write(u'move "{}" "{}"\n'.format(upath, bad + u'\\' + file_replace))
                else:
                    out.write(u':: don\'t touch {}\n'.format(upath))
            else:
                out.write(u':: cannot match {}\n'.format(upath))
            out.flush()
    out.close()
