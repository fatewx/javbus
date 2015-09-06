__author__ = 'mUSicX'
import urllib2

javbus = "http://www.javbus.in/%s"

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

if __name__ == '__main__':
    test = ['snis-134']

    for name in test:
        page = urllib2.urlopen((javbus % name))
        content = page.read()
        print content

