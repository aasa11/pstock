#!/usr/bin/
#coding=gbk
'''
Created on 2013年11月8日

@summary: 

@author: huxiufeng
'''
import urllib
import os
import threading

url_base = r'http://table.finance.yahoo.com/table.csv?s='

def get_day_onestock(stockname, filename):
    url = url_base + stockname
    if stockname[0] == '6':
        url += '.ss'
    else : 
        url += '.sz'
        
    urllink = urllib.urlopen(url)
    filename = os.path.abspath(filename)
    f = open(filename, 'w')
    f.write(urllink.read())
    f.close()


def thread_day_stocks(stockids, respath, index,threadcount):
    for i in range(index, len(stockids), threadcount):
        stockname = stockids[i]
        filename = os.path.join(os.path.abspath(respath), stockname+'.csv')
        print "get day datas : ", stockname, " , ",filename
        get_day_onestock(stockname, filename)
        

def get_day_stocks(cnffile, respath, threadcount = 1):
    rf = open(os.path.abspath(cnffile), 'r')
    stockids = []
    for line in rf.readlines():
        stockids.append(line[0:6])
    
    thdlist = []
        
    for index in range(threadcount):
        threadhandle = threading.Thread(target=thread_day_stocks, args=(stockids, respath, index, threadcount))
        threadhandle.start()
        thdlist.append(threadhandle)
        
    for handle in thdlist:
        handle.join()
    
        



#----------------------It is a split line--------------------------------------

def main():
#     stockname = '600000'
#     filename = 'res/600000.csv'
#     get_day_onestock(stockname, filename)
    cnffile = r'cnf/corp_codes.csv'
    respath = r'res'
    get_day_stocks(cnffile, respath, 3)
    
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"