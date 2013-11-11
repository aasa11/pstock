#!/usr/bin/
#coding=gbk
'''
Created on 2013/08/20

@summary: 

@author: huxiufeng
'''
import sinastock
import time
import copy


STOCKENGINE = sinastock.onestocksina


class stdata:
    def __init__(self, lst,timegap = 30):
        self.stlst = lst
        self.stock = sinastock.onestocksina('', timegap)
        self.gap = timegap
        
    def revloop(self):
        titles = []
        while True :
            datas = []
            for st in self.stlst :
                self.stock.getdata(st)
                if len(titles) <= 0:
                    titles = copy.deepcopy(self.stock.dt.parttitle)
                datas.append(self.stock.dt.partdata)
            self.printdata(titles, datas)
            time.sleep(self.gap)
            
    def printdata(self, titles, datas):
        for idx, v in enumerate(titles):
            strs = ''
            strs += '%4s: '%v
            for data in datas:
                strs += '%-*s|'%(8,data[idx])
            print strs
        print "-"*(11*(len(datas)+1))


#----------------------It is a split line--------------------------------------

def main():
    #'sz002024'
    stlst = ['sz000002', 'sh600756', 'sh600675', 'sh600830','sz300226','sh000001','sh600400']
    st = stdata(stlst)
    st.revloop()
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"