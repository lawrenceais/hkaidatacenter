# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:00:33 2020

@author: lawre
"""

import googleDriveApi as drive
import getStockTransaction as hkex
import convertHtmlText as stext
import time

def getSingleData(localfolder,hkexpath,mYear,mMonth):
    hkex.getStockDaily(localfolder,hkexpath,mYear,mMonth)
    stext.convertCSV(localfolder, mYear, mMonth)
    drive.uploadStockFiles(localfolder,mYear,mMonth)

def getMultipleData(localfolder,hkexpath,mYear,sMonth, eMonth):
    for mm in range (sMonth,(eMonth+1)):       
        hkex.getStockDaily(localfolder,hkexpath,mYear,mm)
        stext.convertCSV(localfolder, mYear, mm)
        drive.uploadStockFiles(localfolder,mYear,mm)
        

if __name__ == '__main__':
    
    tic = time.time()
    
    hkex_path = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
    local_folder = "dailyQuotations"
    
    getSingleData(local_folder, hkex_path, 2020, 10)
    #getMultipleData(local_folder, hkex_path, 2019, 1, 6)
    
    toc = time.time()
    elapsed_time = toc - tic
    print(elapsed_time)