#!/usr/bin/
#coding=gbk
'''
Created on 2013年11月11日

@summary: 

@author: huxiufeng
'''

import os
import time

class st_para:
    def __init__(self, name=None, date=None, v_open=None, 
                 v_close=None, v_high=None, v_low=None, 
                 volum=None, v_adjclose=None, index = 0):
        self.name = name
        self.date = date
        self.v_open = v_open
        self.v_cloes = v_close
        self.v_high = v_high
        self.v_low = v_low
        self.volum = volum
        self.v_adjclose = v_adjclose
        self.index = index
        
    def get_data(self, datas,index = 0):
        datalst = datas.split(',')
        
        if len(datalst) < 7:
            return False
        self.date =  time.strptime(datalst[0], "%Y-%m-%d")
        self.v_open = float(datalst[1])
        self.v_high = float(datalst[2])
        self.v_low = float(datalst[3])
        self.v_close = float(datalst[4])
        self.volum = int(datalst[5])
        self.v_adjclose = float(datalst[6])
        self.index = index
        
        if self.volum <= 0:
            return False
        return True

         


class st_one:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        
    def imp_data(self):
        self.datalst = []
        f = open(self.filename, 'r')
        for line in f.readlines():
            if line.startswith('Date'):
                continue
            onedata = st_para()
            #print line
            rt = onedata.get_data(line)
            if not rt:
                self.datalst.append(onedata)
                #print onedata.date
        
        self.datalst.sort(key=lambda x: x.date)
        
    def get_ratio(self):
        
        

    def draw_dayline(self):
        import matplotlib.pyplot as plt
        plt.figure(1)
        plt.plot(range(len(self.datalst)), [dt.v_close for dt in self.datalst])
        plt.show()
        
        
    
            
             

#----------------------It is a split line--------------------------------------

def main():
    filename = 'res/600000.csv'
    st = st_one(filename)
    st.imp_data()
    st.draw_dayline()
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"