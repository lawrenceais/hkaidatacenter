# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:04:51 2020

@author: lawre
"""

import urllib3
import shutil

hkexpath = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
datafilename = "d200918e.htm"
localfolder = "dailyQuotations"

url = hkexpath + datafilename
localfilename = localfolder + "/" + datafilename



http = urllib3.PoolManager()



with open(localfilename, 'wb') as out:
    r = http.request('GET', url, preload_content=False)
    shutil.copyfileobj(r, out)