# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:00:33 2020

@author: lawre
"""

import googleDriveApi as drive
import getStockTransaction as hkex
import convertHtmlText as stext
import time



if __name__ == '__main__':
    
    t = time.process_time()
    hkexpath = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
    localfolder = "dailyQuotations"
    
    
    mYear = 2020
    mMonth = 10
    hkex.getStockDaily(localfolder,hkexpath,mYear,mMonth)
    stext.convertCSV(localfolder, mYear, mMonth)
    drive.uploadStockFiles(localfolder,mYear,mMonth)
    
    """
    mYear = 2019
    for mm in range (4,7):
       
        hkex.getStockDaily(localfolder,hkexpath,mYear,mm)
        stext.convertCSV(localfolder, mYear, mm)
        drive.uploadStockFiles(localfolder,mYear,mm)
    """
    elapsed_time = time.process_time() - t
    print(elapsed_time)