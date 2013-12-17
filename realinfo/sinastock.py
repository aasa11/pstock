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
        
#    0����������·������Ʊ���ƣ� 
#    1����27.55�壬���̣� 
#    2����27.25�壬�����̣� 
#    3����26.91�壬��ǰ�ۣ� 
#    4����27.55�壬����ߣ� 
#    5����26.20�壬����ͣ� 
#    6����26.91�壬����ۣ� 
#    7����26.92�壬����ۣ�  
#    8����22114263�壬�ɽ��������ڹ�Ʊ������һ�ٹ�Ϊ������λ��������ʹ��ʱ��ͨ���Ѹ�ֵ����һ�٣� 
#    9����589824680�壬�ɽ����λΪ��Ԫ����Ϊ��һĿ��Ȼ��ͨ���ԡ���Ԫ��Ϊ�ɽ����ĵ�λ������ͨ���Ѹ�ֵ����һ��  
#    10����4695�壬����һ������4695�ɣ���47�� 
#    11����26.91�壬��һ�� 
#    12����57590�壬������� 
#    13����26.90�壬����� 
#    14����14700�壬�������� 
#    15����26.89�壬������ 
#    16����14300�壬�����ġ� 
#    17����26.88�壬���ļ� 
#    18����15100�壬�����塱 
#    19����26.87�壬�����  
#    20����3100�壬����һ���걨3100�ɣ���31�֣� 
#    21����26.92�壬��һ��  
#    (22, 23), (24, 25), (26,27), (28, 29)�ֱ�Ϊ���������������ĵ������ 
#    30����2008-01-11�壬���ڣ�
#    31����15:05:32�壬ʱ��
    
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