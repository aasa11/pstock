#!/usr/bin/
#coding=gbk

'''
@summary: 

@author: huxiufeng
'''
from st_element import st_element
from static_define import *
from st_calc import st_calc
from st_calc2 import st_calc2
import os
import sys
import time

#----------------------It is a split line--------------------------------------
class st_stock:
    def __init__(self, names = None, ids = None):
        self.st_name = names
        self.st_id = ids
        self.st_lst = []
        
    def add_element(self, ele):
        ele.st_index = len(self.st_lst)
        self.st_lst.append(ele)
        
    def sort_element(self):
        self.st_lst.sort(key=lambda st : st.get_date())
        for i in range(len(self.st_lst)):
            self.st_lst[i].st_index=i
    
    def pt_brief(self):
        print "name: [", self.st_name, "]", \
              "id: [", self.st_id, "]", \
              "counts: [", len(self.st_lst), "]"
          
    def pt(self):
        self.pt_brief()
        for st in self.st_lst:
            st.pt()
            
    def imp_from_cvs(self, filepath):
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            print "file: [", filepath, "] is not exist."
            return False
        
        f = open(filepath, 'r')
        
        #print "import from [", filepath,"]..."
        for line in f:
            if line.startswith("Date"):
                continue
            lst = line.split(',')
            #need to remove useless lines, volumn is zero
            if int(lst[5]) <= 0:
                continue
            ele = st_element()
            ele.set_data(str(lst[0]),           #date
                         float(lst[1]),         #open
                         float(lst[4]),         #close
                         float(lst[2]),         #high
                         float(lst[3]),         #buttom
                         int(lst[5]),           #volumn
                         float(lst[6]))         #adjclose
            self.add_element(ele)
        
        f.close()
        
        self.sort_element()
        self.rate_common()
        
    
    def imp_from_cvs_bytime(self, filepath,starttime):
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            print "file: [", filepath, "] is not exist."
            return False
        
        f = open(filepath, 'r')
        
        starttime = time.strptime(starttime, "%Y-%m-%d")
        #print "import from [", filepath,"]..."
        for line in f:
            if line.startswith("Date"):
                continue
            
            lst = line.split(',')
            t = time.strptime(lst[0], "%Y-%m-%d")
            if t  < starttime:
                continue
            
            #need to remove useless lines, volumn is zero
            if int(lst[5]) <= 0:
                continue
            ele = st_element()
            ele.set_data(str(lst[0]),           #date
                         float(lst[1]),         #open
                         float(lst[4]),         #close
                         float(lst[2]),         #high
                         float(lst[3]),         #buttom
                         int(lst[5]),           #volumn
                         float(lst[6]))         #adjclose
            self.add_element(ele)
        
        f.close()
        
        self.sort_element()
        self.rate_common() 
    
        
    #-------------common stats----------------#
    def rate_common(self):
        for i in range(1,len(self.st_lst)):
            self.st_lst[i].rate_close(self.st_lst[i-1].st_clos)
            self.st_lst[i].rate_open(self.st_lst[i-1].st_open)
            self.st_lst[i].rate_volumn(self.st_lst[i-1].st_volm)
            self.st_lst[i].rate_swin(self.st_lst[i-1].st_clos)
        self.avg_all_volumn()
            
    
    def avg_all_volumn(self):
        sums = 0
        for l in self.st_lst:
            sums += l.st_volm
            
        self.avg_volm = sums*1.0/len(self.st_lst)
        return self.avg_volm
    
    def get_avg_volm(self,beg, end):
        sums = 0
        for idx in range(beg, end):
            if idx > len(self.st_lst)-1:
                return sums*1.0 / (idx-beg)
            sums += self.st_lst[idx].st_volm
        return sums*1.0 / (end-beg)
    
    #-------------postion function----------------#
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
        
    def pos_threadhold_count(self, 
                       pos, rng, loc=G_POS_TYPE[0], 
                       cmplst=[]):
        if len(cmplst) <= 0:
            return None
        
        (beg, end) = self.get_pos_range(pos, rng, loc)
        sums = 0
        for idx in range(beg, end):
            isok = True
            for cmpimpl in cmplst:
                (_, dtok) = cmpimpl.get_threadhold(self.st_lst[idx])
                if not dtok: 
                    isok = False
                    break
            if isok:
                sums += 1
        return sums  
    
    def pos_calc_max_min(self,
                         pos, rng, loc = G_POS_TYPE[0],
                         stcalc = None):
        (beg, end) = self.get_pos_range(pos, rng, loc)
        (posmax,maxs, posmin, mins) = (None, None, None, None)
        for idx in range(beg, end):
            dt = stcalc.get_calc(self.st_lst[beg:idx+1])
            if posmax is None:
                posmax,maxs, posmin, mins = idx, dt, idx, dt
            elif maxs <dt :
                posmax,maxs = idx, dt
            elif mins >dt :
                posmin, mins = idx, dt      
        return (posmax,maxs, posmin, mins)
    
    def pos_calc_max_min_threadhold(self,
                         pos, rng, loc = G_POS_TYPE[0],
                         stcalc = None,
                         threadhold = None):
        (minthreadhold,maxthreadhold) = threadhold
        (beg, end) = self.get_pos_range(pos, rng, loc)
        (posmax,maxs, posmin, mins) = (None, None, None, None)
        for idx in range(beg, end):
            dt = stcalc.get_calc(self.st_lst[beg:idx+1])
            if posmax is None:
                posmax,maxs, posmin, mins = idx, dt, idx, dt
            if maxs <dt :
                posmax,maxs = idx, dt
            if maxs >=  maxthreadhold:
                return (posmax,maxs, posmin, mins, G_MAXMIN_TYPE[0])
            elif mins >dt :
                posmin, mins = idx, dt
            if mins <=  minthreadhold:
                return (posmax,maxs, posmin, mins, G_MAXMIN_TYPE[1])
        return (posmax,maxs, posmin, mins, G_MAXMIN_TYPE[2])
            
        
         
                        
    #-------------stat function----------------#            
    def stat_rate_count(self, 
                     bfr_rng, bfr_cmplst, bfr_thd, 
                     aft_rng, aft_cmplst, aft_thd): 
        bfr_match = 0
        aft_match = 0
        all_match = 0 
        
        for pos in range(len(self.st_lst)):
            bfr_data = self.pos_threadhold_count(pos, bfr_rng, G_POS_TYPE[0], bfr_cmplst)
            aft_data = self.pos_threadhold_count(pos, aft_rng, G_POS_TYPE[1], aft_cmplst)
            
            if bfr_data >= bfr_thd:
                bfr_match += 1
            if aft_data >= aft_thd:
                aft_match +=1
            if bfr_data >= bfr_thd and aft_data >= aft_thd:
                all_match += 1
        return bfr_match, aft_match, all_match
    
    #-------------stat formula----------------#
    def stat_formula(self, 
                     bfr_rng, bfr_cmplst, bfr_thd,
                              bfr_calclst, bfr_calcthreadlst,
                     afr_rng, aft_calclst, aft_calcthreadlst):
        bfr_match = 0
        aft_match_max = {}
        aft_match_min = {}
        all_match_max = {}
        all_match_min = {} 
        for pos in range(len(self.st_lst)):
            isbfrok = False
            bfr_data1 = self.pos_threadhold_count(pos, bfr_rng, G_POS_TYPE[0], bfr_cmplst)
            iscalcok = True
            for idx in range(len(bfr_calclst)):
                rlt = self.pos_calc_max_min(pos, bfr_rng, G_POS_TYPE[0],
                                                       bfr_calclst[idx], 
                                                       )
                if rlt[1] < bfr_calcthreadlst[idx]:
                    iscalcok = False
                    break
            if bfr_data1 >= bfr_thd and iscalcok:
                isbfrok = True
                bfr_match += 1
            for idx in range(len(aft_calclst)):
                if not idx in aft_match_max:
                    aft_match_max[idx] = 0
                    aft_match_min[idx] = 0
                    all_match_max[idx] = 0
                    all_match_min[idx] = 0
                rlt = self.pos_calc_max_min_threadhold(pos, afr_rng, G_POS_TYPE[1],
                                                       aft_calclst[idx], 
                                                       aft_calcthreadlst[idx])
                if rlt[4] == G_MAXMIN_TYPE[0]:
                    aft_match_max[idx] += 1
                    if isbfrok:
                        all_match_max[idx] += 1
                elif rlt[4] == G_MAXMIN_TYPE[1]:
                    aft_match_min[idx] += 1
                    if isbfrok:
                        all_match_min[idx] += 1        

        return (bfr_match, aft_match_max,aft_match_min, all_match_max,all_match_min)
    
    
    #------------specific formula----------------#
    def stat_formula_10day_10up_5down(self,
                                bfr_rng, bfr_cmplst, bfr_thd,
                              bfr_calclst, bfr_calcthreadlst):
        afr_rng = 10
        aft_calclst = [st_calc('r_clos', G_CMP_TYPE[1], G_FETCH_TYPE[0], 0, G_CALC_TYPE[2])]
        aft_calcthreadlst = [(-5.0, 10)]
        
        return self.stat_formula(bfr_rng, bfr_cmplst, bfr_thd,
                              bfr_calclst, bfr_calcthreadlst,
                     afr_rng, aft_calclst, aft_calcthreadlst)
        
            
    #------------specific formula use calc2----------------#            
    def stat_formula_10day_10up_5low(self):
        calc2 = st_calc2(self.st_lst)
        ups = [0,0]
        lows = [0,0]
        medians = [0,0]
        for idx in range(len(calc2.st_lst)):
            (pos, dt) = calc2.get_aft_pos_up_low(idx, 10, 10, -5)
            if dt == G_MAXMIN_TYPE[0]:
                ups[0] += 1
                ups[1] += self.get_avg_volm(idx, pos+1)
            elif dt == G_MAXMIN_TYPE[1]:
                lows[0] += 1
                lows[1] += self.get_avg_volm(idx, pos+1)
            elif dt == G_MAXMIN_TYPE[2]:
                medians[0] += 1
                medians[1] += self.get_avg_volm(idx, pos+1)
        ups[1] = ups[1]*100/ups[0]/self.avg_volm
        lows[1] = lows[1]*100/lows[0]/self.avg_volm
        medians[1] = medians[1]*100/medians[0]/self.avg_volm
        return (ups, lows, medians)
        
    def stat_formula_cond_aft_10day_10up_5low(self, bfr_rng, bfr_rate, bfr_volm):
        calc2 = st_calc2(self.st_lst)
        ups = [0,0]
        lows = [0,0]
        medians = [0,0]
        for idx in range(len(calc2.st_lst)):
            (rate, volm) = calc2.get_bfr_pos_rate_volm(idx, bfr_rng)
            if rate <bfr_rate or volm < bfr_volm*self.avg_volm:
                continue
            (pos, dt) = calc2.get_aft_pos_up_low(idx, 10, 10, -5)
            if dt == G_MAXMIN_TYPE[0]:
                ups[0] += 1
                ups[1] += self.get_avg_volm(idx, pos+1)
            elif dt == G_MAXMIN_TYPE[1]:
                lows[0] += 1
                lows[1] += self.get_avg_volm(idx, pos+1)
            elif dt == G_MAXMIN_TYPE[2]:
                medians[0] += 1
                medians[1] += self.get_avg_volm(idx, pos+1)
        if ups[0] > 0:
            ups[1] = ups[1]*100.0/ups[0]/self.avg_volm
        if lows[0] > 0:
            lows[1] = lows[1]*100.0/lows[0]/self.avg_volm
        if medians[0] > 0:
            medians[1] = medians[1]*100.0/medians[0]/self.avg_volm
        return (ups, lows, medians)
                


#----------------------It is a split line--------------------------------------

def main():
    st = st_stock("test","60000")
    
    filepath = r"res/600004.csv";
    
    st.imp_from_cvs(filepath)
#     st.pt()
#     
#     bfr_cmplst = [st_calc('r_clos', G_CMP_TYPE[1], G_FETCH_TYPE[0], 0),
#                   st_calc('r_swin', G_CMP_TYPE[1], G_FETCH_TYPE[0], 0.5)]
#     
#     aft_cmplst = [st_calc('r_clos', G_CMP_TYPE[1], G_FETCH_TYPE[0], 0)]
#     
#     
#     print st.pos_threadhold_count(50, 10, G_POS_TYPE[0],bfr_cmplst)
#     print st.pos_threadhold_count(50, 10, G_POS_TYPE[1], aft_cmplst)
#     
#     
#     
#     bfr_cmplst = [st_calc('r_clos', G_CMP_TYPE[1], G_FETCH_TYPE[0], 1),
#                   st_calc('r_swin', G_CMP_TYPE[1], G_FETCH_TYPE[0], 2)]
#     
#     aft_cmplst = [st_calc('r_clos', G_CMP_TYPE[1], G_FETCH_TYPE[0], 1)]
#     
#     print st.stat_rate_count(5, bfr_cmplst, 3, 
#                           2, aft_cmplst, 2)
    
    bfr_rng = 10
    bfr_cmplst = [st_calc('r_clos', G_CMP_TYPE[3], G_FETCH_TYPE[0], 0)]
    bfr_thd = 5
    bfr_calclst = [st_calc('r_clos', G_CMP_TYPE[1], G_FETCH_TYPE[0], 1 , G_CALC_TYPE[2])]
    bfr_calcthreadlst = [-6]
    
    print st.stat_formula_10day_10up_5down(bfr_rng, 
                                     bfr_cmplst, bfr_thd, 
                                     bfr_calclst, bfr_calcthreadlst)
    
    
    print st.stat_formula_10day_10up_5low()
    print st.stat_formula_cond_aft_10day_10up_5low(5,5,1.5)

#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"