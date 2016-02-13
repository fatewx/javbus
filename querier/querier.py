#!/usr/local/bin/python
#coding:utf-8
__author__ = 'mUSicX'

import urllib2, re, time, sys

code_regex = re.compile(r"[a-zA-Z][a-zA-Z0-9]{1,4}-?\d{2,5}(?!/)")

javbus = "http://www.javbus.in/%s"
title_regex = re.compile(r'<div class="movie".+?img src="(.+?)".+?title="(.+?)"></a>.+?"movie-code">(.+?)</span>', re.DOTALL)
actress_regex = re.compile(r'id="star-show">演員(.+?)</ul>', re.DOTALL)
name_regex = re.compile(r'star[^"]+" title="(.+?)"', re.DOTALL)

class VideoName:
    def __init__(self, files):
        self.files = files

    def __iter__(self):
        return VideoNameIterator(self.files)

class VideoNameIterator:
    def __init__(self, files):
        self.names = files
        self.index = -1

    def __next__(self):
        self.index += 1
        if len(self.names) <= self.index:
            raise StopIteration
        return self.names[self.index]


if __name__ == "__main__":
    print sys.argv
    file_content = open(sys.argv[1]).read()
    out = open(sys.argv[2], 'w')
    for code_match in code_regex.finditer(file_content) :
        code = code_match.group()
        if "-" not in code:
            code = re.sub(r"(\d+)", r"-\1", code)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'Cookie':'__cfduid=d106d1ad74a87b7b99e9160f80ec2d7bd1441441724', 'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'}
        req = urllib2.Request(javbus % code, headers = header)
        try:
            response = urllib2.urlopen(req)
            content = response.read()
            title_match = title_regex.search(content)
            if title_match:
                image = title_match.group(1)
                title = title_match.group(2)
                code = title_match.group(3)
            actress = []
            actress_match = actress_regex.search(content)
            if actress_match:
                actress_part = actress_match.group(1)
                for name_match in name_regex.finditer(actress_part):
                    actress.append(name_match.group(1))
            out.write("{}|{}|{}|{}\n".format(code, ",".join(actress),title,image))
            print "doing %s successful" % code
            time.sleep(1)
            out.flush()
        except:
            print "doing %s failed" % code
    out.close()
