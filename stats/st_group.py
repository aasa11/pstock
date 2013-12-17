#!/usr/bin/
#coding=gbk

'''
@summary: 

@author: huxiufeng
'''

from st_stock import st_stock
from st_element import st_element
from static_define import *
from st_calc import st_calc
import os
import sys

#----------------------It is a split line--------------------------------------
class st_group:
    def __init__(self, index = 0, workdir = 'res'):
        self.index = index
        self.st_dic = {}
        self.set_workdir(workdir)

    
    def set_workdir(self, workdir):
        workdir = os.path.abspath(workdir)
        if not os.path.exists(workdir) or not os.path.isdir(workdir):
            print "workdir : [", workdir ,"] is unavailable."
            return False
        self.st_workdir = workdir
        return True 
    
    def add_stock(self, ststock):
        self.st_dic[ststock.st_id] = ststock
        
    def imp_stock_from_dir(self):
        idx = 0
        print "import working dir is [", self.st_workdir,"]"
        for filepath in os.listdir(self.st_workdir):
            print filepath
            absfilepath = os.path.join(self.st_workdir, filepath)
            if not os.path.exists(absfilepath):
                print "[",absfilepath,"] is not exist"
                continue
            ids = os.path.splitext(filepath)[0]
            ststock = st_stock(None, ids)
            print "import file : [", ids,"]..."
            ststock.imp_from_cvs(absfilepath)
            self.add_stock(ststock)
            #print "import file : [", ids,"] end"
            idx += 1
        
        print "Total imported [",idx,"] files."
        
    def imp_stock_from_dir_bytime(self, starttime):
        idx = 0
        print "import working dir is [", self.st_workdir,"]"
        for filepath in os.listdir(self.st_workdir):
            #print filepath
            absfilepath = os.path.join(self.st_workdir, filepath)
            if not os.path.exists(absfilepath):
                print "[",absfilepath,"] is not exist"
                continue
            ids = os.path.splitext(filepath)[0]
            ststock = st_stock(None, ids)
            #print "import file : [", ids,"]..."
            ststock.imp_from_cvs_bytime(absfilepath, starttime)
            self.add_stock(ststock)
            #print "import file : [", ids,"] end"
            idx += 1
        
        print "Total imported [",idx,"] files." 
        
    def pt_brief(self):
        print "group idx : [", self.index,"] ", \
              "base dir : [", self.st_workdir,"] " 
        for _, v in self.st_dic.items():
            v.pt_brief()
            
    def pt(self):
        print "group idx : [", self.index,"] ", \
              "base dir : [", self.st_workdir,"] " 
        for _, v in self.st_dic.items():
            v.pt()
            





#----------------------It is a split line--------------------------------------

def main():
    workdir = 'res'
    grp = st_group(1, workdir)
    grp.imp_stock_from_dir_bytime("2011-01-01")
    #grp.imp_stock_from_dir()
    #grp.pt_brief()
    
    totals = [[0,0],[0,0],[0,0]]
    for ids, st in grp.st_dic.items():
        #print "ids : [", ids,"] :"
        #dt = st.stat_formula_10day_10up_5low()
        dt = st.stat_formula_cond_aft_10day_10up_5low(5, 0, 2)
        #print dt
        for i in range(3):
            for j in range(2):
                totals[i][j] += dt[i][j]
    for i in range(3):
        for j in range(2):
            totals[i][j] = totals[i][j] / len(grp.st_dic)
    print "total is :"
    print totals
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"