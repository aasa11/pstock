#!/usr/bin/
#coding=gbk

'''
@summary: 

@author: huxiufeng
'''

import time
from static_define import *
from st_calc import st_calc
#----------------------It is a split line--------------------------------------
class st_element:
    def __init__(self):
        self.st_date = None
        self.st_index = 0
        #-----base info define-------#
        self.st_open = 0.0
        self.st_clos = 0.0
        self.st_high = 0.0
        self.st_butt = 0.0
        self.st_volm = 0
        self.st_adjc = 0.0
        #-----Rate define-------#
        self.r_clos = 0.0
        self.r_open = 0.0
        self.r_volm = 0.0
        self.r_swin = 0.0
        
    def set_data(self,date = None, opens = 0, close = 0, high = 0, buttom = 0, volumn = 0, adjc = 0):
        self.st_date = date
        self.st_open = opens
        self.st_clos = close
        self.st_high = high
        self.st_butt = buttom
        self.st_volm = volumn
        self.st_adjc = adjc
        
    def set_index(self, index):
        self.st_index = index
        
    def get_date(self):
        if self.st_date is None:
            return None
        t = time.strptime(self.st_date, "%Y-%m-%d")
        return t
        
    def pt(self):
        print "index: [", self.st_index, "]", \
              "date: [", self.st_date, "]", \
              "open: [", self.st_open , "]", \
              "close: [", self.st_clos , "]", \
              "high: [", self.st_high , "]", \
              "buttom: [", self.st_butt , "]", \
              "volumn: [", self.st_volm , "]", \
              "adjclose: [", self.st_adjc, "]", \
              "|| r_open: [", self.r_open, "]", \
              "r_close: [", self.r_clos, "]", \
              "r_volumn: [", self.r_volm, "]", \
              "r_swing: [", self.r_swin, "]"
              
              
    #-------------common stats----------------#
    def rate_close(self, bfr_close = None):
        if bfr_close is None:
            self.r_clos = 0.0
        else:
            self.r_clos = (self.st_clos - bfr_close) *100.0 / bfr_close     
        return self.r_clos
    
    def rate_open(self, bfr_open = None):
        if bfr_open is None:
            self.r_open = 0.0
        else:
            self.r_open = (self.st_open - bfr_open) *100.0 / bfr_open 
        return self.r_open
    
    def rate_volumn(self, bfr_volumn = None):
        if bfr_volumn is None:
            self.r_volm = 0.0
        else:
            self.r_volm = (self.st_volm - bfr_volumn) *100.0 / bfr_volumn 
        return self.r_volm
    
    def rate_swin(self, bfr_close = None):
        if bfr_close is None:
            self.r_swin = (self.st_high - self.st_butt)*100.0 / self.st_open
        else:
            self.r_swin = (self.st_high - self.st_butt)*100.0 / bfr_close     
        return self.r_swin
    
    
    
    #-------------common threadhold----------------#
    def get_threadhold(self, attr_name, 
                       cmptype = G_CMP_TYPE[1], 
                       fetchtype = G_FETCH_TYPE[0], 
                       threadhold = 0.0):
        calc = st_calc(attr_name, cmptype, fetchtype, threadhold)
        return calc.get_threadhold(self)
        
            

#----------------------It is a split line--------------------------------------

def main():
    st = st_element()
    st.pt()
    
    st.set_data("2010-3-17", 10, 10.5, 10.8, 9.4, 2543312, 7.6)
    st.pt()
    
    t = st.get_date()
    print t
    
    
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"