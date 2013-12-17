#!/usr/bin/
#coding='GBK'
'''
Created on 2013/08/08

@summary: test sina stock interface 

@author: huxiufeng
'''

import urllib2
import xmlrpclib
import time
import re
import codecs




def getxmlmethod(spath):
    sp = xmlrpclib.ServerProxy(spath,
                            allow_none = True )
    print sp.system.listMethods()



def getrealdata(sites ,sname):
    page = urllib2.urlopen(sites+sname, timeout = 10)
    data = page.read()
    return data


def test():
    strs = ''
    r = re.compile(r'=\"([\S\s]*)\";$')
    pure = r.findall(strs)
    print pure


def getsinadata(sname):
    sites = r"http://hq.sinajs.cn/list="
    data = getrealdata(sites,sname)
    r = re.compile(r'=\"([\S\s]*)\";$')
    pure = r.findall(data)[0]
    lst = pure.decode('gbk')
    print lst
    purelst = lst.split(',')
    print purelst
    print purelst[0].decode('gbk')

def getqqdata(sname):
    sites = r"http://qt.gtimg.cn/q="
    data = getrealdata(sites,sname)
    r = re.compile(r'=\"([\S\s]*)\";$')
    pure = r.findall(data)[0]
    print pure.decode('gbk')    

#----------------------It is a split line--------------------------------------

def main():
    sname = 'sz000002'
    while True:
        getsinadata(sname)
        time.sleep(5)
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"