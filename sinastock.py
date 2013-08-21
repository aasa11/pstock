#!/usr/bin/
#coding=gbk
'''
Created on 2013/08/13

@summary: 

@author: huxiufeng
'''

import urllib2
import re
import time
import copy

class sinadata():
    def __init__(self, sname, lst):
        self.predef()
        self.series = sname
        self.lst = copy.deepcopy(lst)
        self.doformula()
        self.printlst = [31,0,1,2,3,4,5]
        
#    0：”大秦铁路”，股票名称； 
#    1：”27.55″，今开盘； 
#    2：”27.25″，昨收盘； 
#    3：”26.91″，当前价； 
#    4：”27.55″，今最高； 
#    5：”26.20″，今最低； 
#    6：”26.91″，买入价； 
#    7：”26.92″，买出价；  
#    8：”22114263″，成交量，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百； 
#    9：”589824680″，成交额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；  
#    10：”4695″，“买一”申请4695股，即47手 
#    11：”26.91″，买一价 
#    12：”57590″，“买二” 
#    13：”26.90″，买二价 
#    14：”14700″，“买三” 
#    15：”26.89″，买三价 
#    16：”14300″，“买四” 
#    17：”26.88″，买四价 
#    18：”15100″，“买五” 
#    19：”26.87″，买五价  
#    20：”3100″，“卖一”申报3100股，即31手； 
#    21：”26.92″，卖一价  
#    (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况” 
#    30：”2008-01-11″，日期；
#    31：”15:05:32″，时间
    
    def doformula(self):
        self.getpercent(self.lst)
        self.getbuyall(self.lst)
        self.getsellall(self.lst)
        self.getbtos(self.buyall, self.sellall)
                 
    def getpercent(self, lst):
        self.percent = (float(lst[3])- float(lst[2]))/float(lst[2])* 100.0
        
    def getbuyall(self,lst):
        self.buyall = 0
        for i in xrange(10,19,2):
            self.buyall += float(lst[i])
    
    def getsellall(self, lst):
        self.sellall = 0
        for i in xrange(20,29,2):
            self.sellall += float(lst[i])
            
    def getbtos(self, buyall,sellall):
        if sellall <= 0:
            self.btos = -1
            return
        self.btos = buyall*1.0/sellall
        
    def setprintlist(self,lst):
        self.printlst = copy.deepcopy(lst)
    
    def predef(self):
        self.des = []
        self.des.append('name')
        self.des.append('open')
        self.des.append('bfcl')
        self.des.append('nowp')
        self.des.append('high')
        self.des.append('lows')
        self.des.append('buy0')
        self.des.append('sel0')
        self.des.append('colm')
        self.des.append('mnys')
        self.des.append('by1c')
        self.des.append('by1m')
        self.des.append('by2c')
        self.des.append('by2m')
        self.des.append('by3c')
        self.des.append('by3m')
        self.des.append('by4c')
        self.des.append('by4m')
        self.des.append('by5c')
        self.des.append('by5m')
        self.des.append('sl1c')
        self.des.append('sl1m')
        self.des.append('sl2c')
        self.des.append('sl2m')
        self.des.append('sl3c')
        self.des.append('sl3m')
        self.des.append('sl4c')
        self.des.append('sl4m')
        self.des.append('sl5c')
        self.des.append('sl5m')
        self.des.append('date')
        self.des.append('time')

    
    def printdata(self):
        print self.series
        for idx, m in enumerate(self.des):
            print m, " : ", self.lst[idx]
        print '\n'
        
    def printpartdata(self):
        print self.series
        for idx in self.printlst :
            print self.des[idx], ' : ', self.lst[idx]
        print 'per : ', self.percent
        print 'btos : ', self.btos
    
    def getparttitle(self):
        self.parttitle = []
        self.parttitle.append("code")
        for idx in self.printlst :
            self.parttitle.append(self.des[idx])
        self.parttitle.append("per")
        self.parttitle.append("btos")
            
    def getpartdata(self):
        self.partdata = []
        self.partdata.append(self.series)
        for idx in self.printlst :
            self.partdata.append(str(self.lst[idx]))
        self.partdata.append('%.4f'%self.percent)
        self.partdata.append('%.4f'%self.btos)
    
#----------------------It is a split line--------------------------------------
class onestocksina:
    def __init__(self,sname, gap = 5):
        self.sites = r'http://hq.sinajs.cn/list='
        self.r = re.compile(r'=\"([\S\s]*)\";$')
        self.coding = 'gbk'
        self.spcode = ','
        self.timeout = 10
        self.data = []
        self.sname = sname
        self.gap = gap
        
    def geturl(self, sname):
        page = urllib2.urlopen(self.sites+sname, timeout = self.timeout)
        self.sname = sname
        data = page.read()
        return data

    def getdata(self, sname):
        data = self.geturl(sname)
        lst = self.r.findall(data)
        if len(lst) <= 0:
            return
        purelst = lst[0].split(self.spcode)
        self.formdata(purelst)
        
    def formdata(self, lst):
        self.dt = sinadata(self.sname, lst)
        #self.dt.printpartdata()
        self.dt.getparttitle()
        self.dt.getpartdata()
        
            
    def revloop(self):
        while True:
            self.getdata(self.sname)
            time.sleep(self.gap)

#----------------------It is a split line--------------------------------------

def main():
    sname ='sz000002'
    onest = onestocksina(sname)
    onest.revloop()
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"