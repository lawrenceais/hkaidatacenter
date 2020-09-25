# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:04:51 2020

@author: lawre
"""

import urllib3
import shutil
import pathlib


hkexpath = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
datafilename = "d200918e.htm"
localfolder = "dailyQuotations"

url = hkexpath + datafilename
localfilename = localfolder + "/" + datafilename

searchYear = "20"
searchMonth = "09"

for dd in range(1, 32):
    datafilename = "d" + searchYear + searchMonth+str(dd).zfill(2) + "e.htm"
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

#http = urllib3.PoolManager()



with open(localfilename, 'wb') as out:
    r = http.request('GET', url, preload_content=False)
    shutil.copyfileobj(r, out)
    
"""
