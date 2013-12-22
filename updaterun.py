#! /usr/bin/env python
#-*- encoding=utf8 -*-
import urllib2
import re
import time
import os.path
import subprocess
import shlex


def download(filename, url):
    """
    download URL and write to file whose name is FILENAME
    success return True
    else return False
    """
    req = urllib2.Request(url)
    try:
        f = urllib2.urlopen(req)
        localfile = open(filename, "wb")
        localfile.write(f.read())
        localfile.close()
    except urllib2.HTTPError, e:
        print "HTTP Error: ", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error: ", e.reason, url
        return False
    return True


def md5sum(filename):
    import hashlib
    return hashlib.md5(open(filename).read()).hexdigest()


def CheckMd5(filename, md5file):
    """
    Check FILENAME file md5sum with md5file
    compare md5sum value and filename
    """
    md5 = md5sum(filename)
    md5con = open(md5file).read().split()
    return md5 == md5con[0] and filename == md5con[1]


def DownCheck(url, chksuffix=".md5"):
    filename = os.path.basename(url)
    md5file = filename + chksuffix
    md5url = url + chksuffix
    if download(filename, url) and download(md5file, md5url):
        if not CheckMd5(filename, md5file):
            print "md5check failed", filename, md5file
            return False
        return True
    else:
        print "download ", url, md5url, " faild"
        return False


def getHref(html, prefix, suffix):
    """
    input: html content, match link prefix and suffix
    find all match href="PREFIX???SUFFIX"
    return max match link
    """
    pattern = re.compile("href=\"" + prefix + ".*" + suffix + "\"")
    filelst = [i[6:-1] for i in pattern.findall(html)]
    return max(filelst)


def CheckNewestName(urlPrefix, filePrefix, fileType):
    download("urllst", urlPrefix)
    return getHref(open("urllst").read(), filePrefix, fileType)


def CheckLocalNewest(pathname, filePrefix, fileType):
    filelst = os.listdir(pathname)
    pattern = re.compile(filePrefix + ".*" + fileType + "$")
    fnlst = [fn for fn in filelst if pattern.match(fn)]
    if fnlst:
        fn = max(fnlst)
        if CheckMd5(fn, fn + ".md5"):
            return fn
    return ""


def replacePID(pid, cmd):
    if pid != 0:
        pid.kill()
    print cmd
    cmd = shlex.split(cmd)
    return subprocess.Popen(cmd)


def runit(urlPrefix, local, filePrefix, fileType):
    pid = 0
    while 1:
        netnew = CheckNewestName(urlPrefix, filePrefix, fileType)
        locnew = CheckLocalNewest(local, filePrefix, fileType)
        if netnew > locnew and DownCheck(urlPrefix + netnew):
            print "update to ", netnew
            locnew = netnew
            cmd = "python " + locnew
            pid = replacePID(pid, cmd)
        if pid == 0:
            cmd = "python " + locnew
            pid = replacePID(pid, cmd)
        time.sleep(10)


def test():
    urlPrefix = "http://home.ustc.edu.cn/~liuyang1/"
    filePrefix = "test_"
    fileType = ".py"
    runit(urlPrefix, ".", filePrefix, fileType)


if __name__ == "__main__":
    test()
