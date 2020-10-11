# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:27:49 2020

@author: lawre
"""

import sqlite3
import os
import datetime


import os
from bs4 import BeautifulSoup
import pathlib
import datetime



def create_stockTable(db_dir, db_name, tb_name):
    database_path = db_dir + "/" + db_name
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS {tab}
              (ID INTEGER PRIMARY KEY AUTOINCREMENT,
               STOCKCODE TEXT,
               SESSION TEXT,
               TYPE TEXT,
               QUANTITY INTEGER,
               PRICE DECIMAL (5,3));'''.format(tab=tb_name))
    print("   Create Table at " + database_path)
   
    conn.commit()
    conn.close()
    
def erase_stockTable(db_dir, db_name, tb_name):
    database_path = db_dir + "/" + db_name
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute('''DELETE FROM {tab}'''.format(tab=tb_name))
    print("   Empty Table at " + database_path)
    
    conn.commit()
    conn.close()
    
def insert_stockTable(db_dir, db_name, tb_name, dataset):
    database_path = db_dir + "/" + db_name
    conn = sqlite3.connect(database_path)
    #c = conn.cursor()
    sql = '''INSERT INTO {tab} (STOCKCODE, SESSION, TYPE, QUANTITY, PRICE) values (?,?,?,?,?)'''.format(tab=tb_name)
    #print(sql)
    
    
    conn.executemany(sql, dataset)
    #c.close()
    conn.commit()
  

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def searchSaleRecords(file_name):
    line_number = 0
    flag_capture = 0
    flag_once = 0
    list_of_results = []
    
    result = ""
    section_separator = "-------------------------------------------------------------------------------"
    data_starting = "CODE  NAME OF STOCK    SALES RECORD"
    data_ending = section_separator
    
   
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
         # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            
            # For each line, check if line contains any string from the list of strings
            if flag_once == 0:                
                if ((flag_capture == 0) and (data_starting in line)):                
                    flag_capture = 1
            
                if ((flag_capture == 1) and (data_ending in line)):
                    flag_capture = 0
                    flag_once = 1
                
            
                if (flag_capture == 1 ):
                    #list_of_results.append(line)
                    data = line.rstrip('\n')
                    #data = line
                    str_stockcode = data[0:5]
                    
                    if (str_stockcode.count(' ') < 5):
                        data = "\n" + data.replace(",","")
                    else:
                        data = data.lstrip()
                        data = data.replace(",","")
                        
                    
                    result += data
                
    # Return list of tuples containing line numbers and lines where string is found
    #return list_of_results
    return result


def getTrade(ttype, stockcode, dataline):
    startMark = ["<", ">[", "]/-//[", "]<"]
    endMark = [">[", "]/-//[", "]<", ">"]
    tradeMarker = ["MA","MT","AT","AA"]
    startpos = dataline.find(startMark[ttype]) + len(startMark[ttype])
    endpos = dataline.find(endMark[ttype],startpos)
    result = []
    datasection = dataline[startpos:endpos]       #find out the section of MA/MT/AT/AA
    lineb = ""
    spacecount = datasection.count(' ')           #inside section, trade is separate by space
    for ki in range(0,(spacecount-1)):
        # " P107500-46.60 P301-46.60 P75000-46.60 4500-47.30 U1500-47.30 "
        startpos = datasection.find(" ",0)   #find the first space, it is starting position
        endpos = datasection.find(" ",1)     #find the next space
        barpos = datasection.find("-",1)     #find the -, it is the separator of QTY-PRICE
        
        rType = datasection[1:2]                  
        if (is_integer(rType)):         #check for trade type
            rQty = datasection[1:barpos]      #if first character is a number, it is normal trade
            rType = "N"
        else:
            rQty = datasection[2:barpos]         
        rPrice = datasection[barpos+1:endpos]    
        
        tradeRecord = (stockcode, tradeMarker[ttype], rType, rQty, rPrice)
        
        result.append(tradeRecord)
        
        datasection = datasection[endpos:]
    
    return result    

def getTradeA(ttype, stockcode, dataline):
    startMark = ["<", ">[", "]/-//[", "]<"]
    endMark = [">[", "]/-//[", "]<", ">"]
    tradeMarker = ["MA","MT","AT","AA"]
    result = []
    for ka in range(0,4):
        startpos = dataline.find(startMark[ka]) + len(startMark[ka])
        endpos = dataline.find(endMark[ka],startpos)
        datasection = dataline[startpos:endpos]       #find out the section of MA/MT/AT/AA
        records = datasection.split(' ')
        markerCount = len(records)
    
        #spacecount = datasection.count(' ')           #inside section, trade is separate by space
        for ki in range(0,markerCount):
            # " P107500-46.60 P301-46.60 P75000-46.60 4500-47.30 U1500-47.30 "
        
            datasection = records[ki]
            #startpos = datasection.find(" ",0)   #find the first space, it is starting position
            #endpos = datasection.find(" ",1)     #find the next space
            barpos = datasection.find("-",1)     #find the -, it is the separator of QTY-PRICE
            if (barpos > 0):                    # if find a bar, it is transaction
                rType = datasection[0:1]                  
                if (is_integer(rType)):         #check for trade type
                    rQty = datasection[0:barpos]      #if first character is a number, it is normal trade
                    rType = "N"
                else:
                    rQty = datasection[1:barpos]         
                rPrice = datasection[barpos+1:]    
        
                tradeRecord = (stockcode, tradeMarker[ka], rType, rQty, rPrice)
        
                result.append(tradeRecord)
        
    
    return result    
            
            
def getSaleRecords(folder_name, file_name, database_folder,  dateinfo):
    #local_file = folder_name + "/" + file_name
    local_file = folder_name + "/" + file_name[0:-4]+".txt"
    local_newfile = folder_name + "/" + file_name[0:-4] +"s.txt"
    local_newfile1 = folder_name + "/" + file_name[0:-4] +"t.txt"
    
    db_name = "st20" + dateinfo[1:5] + ".db" 
    tb_name = dateinfo
    
    create_stockTable(database_folder, db_name, tb_name)
    erase_stockTable(database_folder, db_name, tb_name)
    
    print("    Get html to text")
    SalesRecord = searchSaleRecords(local_file)
    
    '''
    print("    Save to text file")
    with open(local_newfile,'w') as f1:
            f1.write(SalesRecord)
    '''
   
    line_number = 0
    
    print("    Convert text records")
    records = SalesRecord.split('\n')
    markerCount = len(records)
    marker10p = markerCount / 11 
    marker_line = marker10p
         
    print("    Convert records to datebase")
    for ki in range(0, markerCount):
        # Read all lines in the file one by one
        line_number += 1
        
        datasection = records[ki]
        str_stockcode = datasection[0:5]
        if (is_integer(str_stockcode)):
            '''
            OpenAuction = getTrade(0, str_stockcode, datasection)                        
            MorningTrade = getTrade(1, str_stockcode, datasection)
            AfternoonTrade = getTrade(2, str_stockcode, datasection)
            AfternoonAuction = getTrade(3, str_stockcode, datasection)
            result = OpenAuction + MorningTrade + AfternoonTrade + AfternoonAuction
            '''
            result = getTradeA(0, str_stockcode, datasection) 
            
            
            insert_stockTable(database_folder, db_name, tb_name, result)
            
            if (line_number > marker_line):
                markerpercent = line_number // (marker10p / 10)
                print("        Working ... {p}%".format(p=markerpercent))
                marker_line = marker_line + marker10p
            
            
def convertToText(folder_name, file_name):
    local_file = folder_name + "/" + file_name
    local_newfile = folder_name + "/" + file_name[0:-4]+".txt"      
    with open (local_file,"r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        stockfile = soup.get_text()
        newtext = stockfile
        with open(local_newfile,'w') as f1:
            f1.write(newtext)
            
def convertToDb(folderlocation, databaselocation, sYear, sMonth):
    now = datetime.datetime.now()
    endDay = 32
    if (sYear == now.year):
        if (sMonth == now.month):
            endDay = now.day + 1
    
    for dd in range(1,endDay):
        datafile = "d" + str(sYear-2000) + str(sMonth).zfill(2) + str(dd).zfill(2)  #d201005
        datafilename = datafile + "e.htm"                                           #d201005e.htm
        print(datafilename)
        datefolder = str(sYear) + str(sMonth).zfill(2)                              #2010
        localfolder = folderlocation + "/" + datefolder                             #dailyQuotations/2010
        localfilename = localfolder + "/" + datafilename                            #dailyQuotations/2010/d201005e.htm
        file = pathlib.Path(localfilename)
        if file.exists():
            print(localfilename)
            
            convertToText(localfolder, datafilename)
            getSaleRecords(localfolder,datafilename, databaselocation, datafile)     #fill transactions into database
            '''    
            csvfilename = localfolder + "/" + datafilename[0:-4] +"t.csv"
            file_csv = pathlib.Path(csvfilename)
            if file_csv.exists():
                pass
            else:
                convertToText(localfolder, datafilename)
                getSaleRecords(localfolder,datafilename, databaselocation, datafile)     #fill transactions into database
            
                file_t = localfolder + "/" + datafilename[0:-4]+".txt"            
                if os.path.isfile(file_t):
                    os.remove(file_t)
            '''

if __name__ == '__main__':  
    pass
    stockfile = ""
    stockFolder = "dailyQuotations"
    databaseFolder = "../database"
    convertToDb(stockFolder, databaseFolder, 2020, 11)
#    create_stockTable("../database", "st202010.db", "d201009a")
 #   insert_stockTable("../database", "st202010.db", "d201009a", data)
    