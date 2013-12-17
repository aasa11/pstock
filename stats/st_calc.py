#!/usr/bin/
#coding=gbk

'''
@summary: 

@author: huxiufeng
'''

import os
import sys
from static_define import *
#----------------------It is a split line--------------------------------------
class st_calc:
    def __init__(self, attr_name, cmp_type=None, fetch_type = None, threadhold=None, calctype = None):
        self.attr_name = attr_name
        self.cmp_type = cmp_type
        self.fetch_type = fetch_type
        self.threadhold = threadhold
        self.calc_type = calctype
        
    def get_threadhold(self, obj):
        if self.cmp_type is None or \
            self.fetch_type is None or \
            self.threadhold is None:
            return (None, False)
        attr_name = self.attr_name
        cmptype = self.cmp_type
        fetchtype = self.fetch_type
        threadhold = self.threadhold
        
        if not hasattr(obj, self.attr_name):
            print "element has no attribute : [", self.attr_name,"]"
            return (None, False)
        
        data = getattr(obj, attr_name)
        
        cmpresult = False
        if cmptype == G_CMP_TYPE[0]and data == threadhold:
            cmpresult = True
        elif cmptype == G_CMP_TYPE[1] and data > threadhold:
            cmpresult = True
        elif cmptype == G_CMP_TYPE[2] and data >= threadhold:
            cmpresult = True
        elif cmptype == G_CMP_TYPE[3] and data < threadhold:
            cmpresult = True
        elif cmptype == G_CMP_TYPE[4] and data <= threadhold:
            cmpresult = True
            
        if cmpresult:
            if fetchtype == G_FETCH_TYPE[0]:
                return (1, True)
            elif fetchtype == G_FETCH_TYPE[1]:
                return (data,True)
            elif fetchtype == G_FETCH_TYPE[2]:
                return (data,True) 
        else:
            if fetchtype == G_FETCH_TYPE[0]:
                return (0,False)
            elif fetchtype == G_FETCH_TYPE[1]:
                return (0,False)
            elif fetchtype == G_FETCH_TYPE[2]:
                return (None, False) 
        
    def get_calc(self, objlst):
        if self.calc_type is None or len(objlst) <= 0:
            return (0, False)
        sums = 0
        if self.calc_type == G_CALC_TYPE[0]:
            for obj in objlst:
                if not hasattr(obj, self.attr_name):
                    print "element has no attribute : [", self.attr_name,"]"
                    return (None, False)
                sums += getattr(objlst[0], self.attr_name)
            return (sums,True)
        elif self.calc_type == G_CALC_TYPE[1]: 
            if not hasattr(objlst[0], self.attr_name) or \
                not hasattr(objlst[len(objlst)-1], self.attr_name):
                    print "element has no attribute : [", self.attr_name,"]"
                    return (0,False)
            dt0 = getattr(objlst[0], self.attr_name)
            dtn = getattr(objlst[len(objlst)-1], self.attr_name)
            sums = dtn - dt0
            return sums
        elif self.calc_type == G_CALC_TYPE[2]: 
            if not hasattr(objlst[0], self.attr_name) or \
                not hasattr(objlst[len(objlst)-1], self.attr_name):
                    print "element has no attribute : [", self.attr_name,"]"
                    return (0,False)
            dt0 = getattr(objlst[0], self.attr_name)
            dtn = getattr(objlst[len(objlst)-1], self.attr_name)
            if dt0 == 0:
                sums = 0
            else:
                sums = (dtn - dt0)*100.0/dt0
            return sums

    
    
        


#----------------------It is a split line--------------------------------------

def main():
    pass
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"