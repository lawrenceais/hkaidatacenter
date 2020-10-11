# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:00:33 2020

@author: lawre
"""

import googleDriveApi as drive
import getStockTransaction as hkex
import convertHtmlText as stext
import storeDatabase as db
import time
import datetime

def time_conversion(sec_input):
    sec = int(sec_input)
    sec_value = sec % (24 * 3600)
    hour_value = sec_value // 3600
    sec_value %= 3600
    min_value = sec_value // 60
    sec_value %= 60
   
    result = str(hour_value).zfill(2) + ":" + str(min_value).zfill(2) + ":" + str(sec_value).zfill(2)
   
    return result
  

def getSingleData(localfolder,hkexpath,mYear,mMonth):
    hkex.getStockDaily(localfolder,hkexpath,mYear,mMonth)
    stext.convertCSV(localfolder, mYear, mMonth)
    drive.uploadStockFiles(localfolder,mYear,mMonth)

def getMultipleData(localfolder,hkexpath,mYear,sMonth, eMonth):
    for mm in range (sMonth,(eMonth+1)):       
        hkex.getStockDaily(localfolder,hkexpath,mYear,mm)
        stext.convertCSV(localfolder, mYear, mm)
        drive.uploadStockFiles(localfolder,mYear,mm)
        
def getOneMonthDataDb(localfolder, dbfolder, hkexpath, mYear, mMonth):
    hkex.getStockDaily(localfolder,hkexpath, mYear, mMonth)
    #stext.convertCSV(localfolder, mYear, mMonth)
    db.convertToDb(localfolder, dbfolder, mYear, mMonth)
    
def getMultiMonthDataDb(localfolder, dbfolder, hkexpath, mYear, mMonth, eMonth):
    for mm in range (sMonth,(eMonth+1)): 
        hkex.getStockDaily(localfolder,hkexpath, mYear, mm)
        #stext.convertCSV(localfolder, mYear, mMonth)
        db.convertToDb(localfolder, dbfolder, mYear, mm)

if __name__ == '__main__':
    
    tic = time.time()
    
    hkex_path = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
    local_folder = "dailyQuotations"
    database_folder = "../database"
    wYear = 2020
    wMonth = 9
    getOneMonthDataDb(local_folder, database_folder, hkex_path, wYear, wMonth)
    #getSingleData(local_folder, database_folder, hkex_path, 2020, 10)
    #getMultipleData(local_folder, hkex_path, 2019, 1, 6)
    
    toc = time.time()
    elapsed_time = (toc - tic)
    
    logTime = datetime.datetime.now()
    logHistory = logTime.strftime("%m/%d/%Y %H:%M:%S  ") 
    logHistory = logHistory + "Working for (" + str(wYear) + "-" + str(wMonth).zfill(2) + ") "
    logHistory = logHistory + "Duration: " + time_conversion(elapsed_time) + "\n"
    print(logHistory)
    
    with open("getDatalog.txt",'a') as f1:
            f1.write(logHistory)
    
    #2020-10         209
    #2020-09  2417   1094
    #2020-08  1100 
    #2020-07  18.6 