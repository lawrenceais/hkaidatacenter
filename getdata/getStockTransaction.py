# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:04:51 2020

@author: lawre
"""
import os
import urllib3
import shutil
import pathlib
import datetime

def getStockDailyQuotations(localpath, urlpath, datafilename):
    result = False
    localFileValid = False
    url = urlpath + datafilename
    localfilename = localpath + "/" + datafilename
    file = pathlib.Path(localfilename)
    if file.exists():
        print("    File exist")
        file_info = os.stat(localfilename)
        print(file_info.st_size)
        localFileSize = file_info.st_size
        if (localFileSize > 10000):
            localFileValid = True
    if (localFileValid == False):
        print("    Get File ...")
        http = urllib3.PoolManager()
        with open(localfilename, 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            print("    Save File.")
            shutil.copyfileobj(r, out)

def getStockDaily(localpath, urlpath, sYear, sMonth):
    now = datetime.datetime.now()
    #print(now.year)
    #print(now.month)
    #print(now.day)
    
    endDay = 32
    if (sYear == now.year):
        if (sMonth == now.month):
            endDay = now.day + 1
    
    for dd in range(1,endDay):
        datafilename = "d" + str(sYear-2000) + str(sMonth).zfill(2) + str(dd).zfill(2) + "e.htm"
        print(datafilename)
        getStockDailyQuotations(localfolder,hkexpath,datafilename)
        

if __name__ == '__main__':   
    hkexpath = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
    localfolder = "dailyQuotations"
    
    #datafilename = "d200918e.htm"
    
    getStockDaily(localfolder,hkexpath,2019,3)
    
    """
    searchYear = "20"
    searchMonth = "09"
    for dd in range(1, 5):
        datafilename = "d" + searchYear + searchMonth+str(dd).zfill(2) + "e.htm"
        print(datafilename)
        getStockDailyQuotations(localfolder,hkexpath,datafilename)

"""

"""
hkexpath = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
datafilename = "d200918e.htm"
localfolder = "dailyQuotations"

url = hkexpath + datafilename
localfilename = localfolder + "/" + datafilename

searchYear = "20"
searchMonth = "09"

for dd in range(1, 32):
    datafilename = "d" + searchYear + searchMonth+str(dd).zfill(2) + "e.htm"  #"d200918e.htm"
    print(datafilename)
    try:
        url = hkexpath + datafilename
        localfilename = localfolder + "/" + datafilename
        
        file = pathlib.Path(localfilename)
        if file.exists():
            print("    File exist")
        else:
            print("    Get File ...")
        
        
            http = urllib3.PoolManager()
            with open(localfilename, 'wb') as out:
                r = http.request('GET', url, preload_content=False)
                print("    Save File.")
                shutil.copyfileobj(r, out)
            
        
        
    except:
        print("Date is not valid!")
    
"""


