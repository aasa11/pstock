#!/usr/bin/
#coding=gbk

'''
@summary: 

@author: huxiufeng
'''
import os
from st_element import *

#----------------------It is a split line--------------------------------------
class st_calc2:
    def __init__(self, st_lst):
        self.st_lst = st_lst
    
    def get_pos_range(self, pos, rng, loc=G_POS_TYPE[0]):
        '''get the static range by the loc(bfr or aft)'''
        if loc == G_POS_TYPE[0]:
            if pos >=len(self.st_lst):
                pos = len(self.st_lst) - 1
            if pos-rng < 0:
                beg = 0
            else:
                beg = pos-rng
            return (beg, pos)
        else:
            if pos < 0:
                pos = 0
            if pos+rng > len(self.st_lst):
                end = len(self.st_lst)
            else:
                end = pos+rng
            return (pos, end)
    
    
    #------------calc functions-------------------------#
    def get_aft_pos_up_low(self, pos, rng, ups, lows):
        (beg, end) = self.get_pos_range(pos, rng, G_POS_TYPE[1])
        start_dt = 0
        if beg == 0:
            start_dt = self.st_lst[0].st_open
        else :
            start_dt = self.st_lst[beg-1].st_clos
        if start_dt ==0:
            #print "start data error : [",start_dt,"]"
            return (None,None)
            
        for idx in range(beg, end):
            dt = (self.st_lst[idx].st_clos - start_dt)*100.0 / start_dt
            if dt >= ups:
                return (idx, G_MAXMIN_TYPE[0])
            elif dt <=lows:
                return (idx, G_MAXMIN_TYPE[1])
        return (end, G_MAXMIN_TYPE[2])
            
    def get_bfr_pos_rate_volm(self, pos, rng):
        (beg, end) = self.get_pos_range(pos, rng, G_POS_TYPE[0])
        start_dt = 0
        if beg == 0:
            start_dt = self.st_lst[0].st_open
        else :
            start_dt = self.st_lst[beg-1].st_clos
        if start_dt ==0:
            #print "start data error : [",start_dt,"]"
            return (None,None)
        
        sum_volm = 0
        for idx in range(beg, end):    
            sum_volm += self.st_lst[idx].st_volm
        dt = (self.st_lst[end-1].st_clos - start_dt)*100.0 / start_dt
        return (dt, sum_volm)
        

#----------------------It is a split line--------------------------------------

def main():
    pass
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"