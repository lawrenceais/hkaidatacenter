# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:00:33 2020

@author: lawre
"""

import googleDriveApi as drive
import getStockTranscation as hkex
import convertHtmlText as stext




if __name__ == '__main__':
    hkexpath = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/"
    localfolder = "dailyQuotations"
    
    hkex.getStockDaily(localfolder,hkexpath,2020,10)
    #drive.main_search_upload("d200902e.htm")