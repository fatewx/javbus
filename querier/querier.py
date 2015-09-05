﻿__author__ = 'mUSicX'

import urllib2, re

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
	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'Cookie':'__cfduid=d106d1ad74a87b7b99e9160f80ec2d7bd1441441724', 'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'}
	req = urllib2.Request(javbus % "snis-412", headers = header)
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
	print "{}|{}|{}|{}".format(code, ",".join(actress),title,image)