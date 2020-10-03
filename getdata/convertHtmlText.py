# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 20:55:13 2020

@author: lawre
"""

from bs4 import BeautifulSoup

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results


def convertToText(folder_name, file_name):
    local_file = folder_name + "/" + file_name
    local_newfile = folder_name + "/" + file_name[0:-4]+".txt"      
    with open (local_file,"r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        newtext = soup.get_text()
        with open(local_newfile,'w') as f1:
            f1.write(newtext)

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
                
def getSaleRecords(folder_name, file_name):
    #local_file = folder_name + "/" + file_name
    local_file = folder_name + "/" + file_name[0:-4]+".txt"
    local_newfile = folder_name + "/" + file_name[0:-4] +"s.txt"
    
    SalesRecord = searchSaleRecords(local_file)
    
    with open(local_newfile,'w') as f1:
            f1.write(SalesRecord)

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def getOpenAuction(stockcode, transactionline):
    startMark = "<"
    endMark = ">["
    startpos = transactionline.find(startMark) + 1
    endpos = transactionline.find(endMark)
    result = ""
    linea = transactionline[startpos:endpos]
    lineb = ""
    spacecount = linea.count(' ')
    for ki in range(0,spacecount-1):
        startpos = linea.find(" ",0)
        endpos = linea.find(" ",1)
        barpos = linea.find("-",1)
        
        linet = linea[1:2]
        if (is_integer(linet)):
            lineb = linea[1:barpos]
            linet = "N"
        else:
            lineb = linea[2:barpos]
        linec = linea[barpos+1:endpos]    
        
        result += stockcode + ",MA," + linet + "," + lineb + "," + linec + "\n"
        linea = linea[endpos:]
    
    return result
    
def getMorningTrade(stockcode, transactionline):
    startMark = ">["
    endMark = "]/-//["
    startpos = transactionline.find(startMark) + 2
    endpos = transactionline.find(endMark)
    result = ""
    linea = transactionline[startpos:endpos]
    lineb = ""
    spacecount = linea.count(' ')
    for ki in range(0,spacecount-1):
        startpos = linea.find(" ",0)
        endpos = linea.find(" ",1)
        barpos = linea.find("-",1)
        
        linet = linea[1:2]
        if (is_integer(linet)):
            lineb = linea[1:barpos]
            linet = "N"
        else:
            lineb = linea[2:barpos]
        linec = linea[barpos+1:endpos]    
        
        result += stockcode + ",MT," + linet + "," + lineb + "," + linec + "\n"
        linea = linea[endpos:]
    
    return result

def getAfternoonAuction(stockcode, transactionline):
    startMark = "]<"
    endMark = ">"
    startpos = transactionline.find(startMark) + 2
    endpos = transactionline.find(endMark,startpos)
    result = ""
    linea = transactionline[startpos:endpos]
    lineb = ""
    spacecount = linea.count(' ')
    for ki in range(0,spacecount-1):
        startpos = linea.find(" ",0)
        endpos = linea.find(" ",1)
        barpos = linea.find("-",1)
        
        linet = linea[1:2]
        if (is_integer(linet)):
            lineb = linea[1:barpos]
            linet = "N"
        else:
            lineb = linea[2:barpos]
        linec = linea[barpos+1:endpos]    
        
        result += stockcode + ",AA," + linet + "," + lineb + "," + linec + "\n"
        linea = linea[endpos:]
    
    return result
    
def getAfternoonTrade(stockcode, transactionline):
    startMark = "]/-//["
    endMark = "]<"
    startpos = transactionline.find(startMark) + 6
    endpos = transactionline.find(endMark)
    result = ""
    linea = transactionline[startpos:endpos]
    lineb = ""
    spacecount = linea.count(' ')
    for ki in range(0,spacecount-1):
        startpos = linea.find(" ",0)
        endpos = linea.find(" ",1)
        barpos = linea.find("-",1)
        
        linet = linea[1:2]
        if (is_integer(linet)):
            lineb = linea[1:barpos]
            linet = "N"
        else:
            lineb = linea[2:barpos]
        linec = linea[barpos+1:endpos]    
        
        result += stockcode + ",AT," + linet + "," + lineb + "," + linec + "\n"
        linea = linea[endpos:]
    
    return result

def getTrade(ttype, stockcode, transactionline):
    startMark = ["<", ">[", "]/-//[", "]<"]
    endMark = [">[", "]/-//[", "]<", ">"]
    tradeMarker = ["MA","MT","AT","AA"]
    startpos = transactionline.find(startMark[ttype]) + len(startMark[ttype])
    endpos = transactionline.find(endMark[ttype],startpos)
    result = ""
    linea = transactionline[startpos:endpos]
    lineb = ""
    spacecount = linea.count(' ')
    for ki in range(0,spacecount-1):
        startpos = linea.find(" ",0)
        endpos = linea.find(" ",1)
        barpos = linea.find("-",1)
        
        linet = linea[1:2]
        if (is_integer(linet)):
            lineb = linea[1:barpos]
            linet = "N"
        else:
            lineb = linea[2:barpos]
        linec = linea[barpos+1:endpos]    
        
        result += stockcode + "," + tradeMarker[ttype] + "," + linet + "," + lineb + "," + linec + "\n"
        linea = linea[endpos:]
    
    return result    
    
def getTransactions(folder_name, file_name):
    local_file = folder_name + "/" + file_name[0:-4] +"s.txt"     
    local_newfile = folder_name + "/" + file_name[0:-4] +"t.csv"   
    line_number = 0
    result = ""
    
    # Open the file in read only mode
    with open(local_file, 'r') as read_obj:
         # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            data = line
            str_stockcode = data[0:5]
            if (is_integer(str_stockcode)):
                #result += format(line_number, '05d') + " " + str_stockcode + "\n"
                #OpenAuction = getOpenAuction(str_stockcode, data)
                #MorningTrade = getMorningTrade(str_stockcode, data)
                #AfternoonTrade = getAfternoonTrade(str_stockcode, data)
                #AfternoonAuction = getAfternoonAuction(str_stockcode, data)
                
                OpenAuction = getTrade(0, str_stockcode, data)
                MorningTrade = getTrade(1, str_stockcode, data)
                AfternoonTrade = getTrade(2, str_stockcode, data)
                AfternoonAuction = getTrade(3, str_stockcode, data)
                result += OpenAuction + MorningTrade + AfternoonTrade + AfternoonAuction
            
    with open(local_newfile,'w') as f1:
            f1.write(result)
            
    
    
    
if __name__ == '__main__':
    
    folder = "dailyQuotations"
    file = "d190506e.htm"
    
    convertToText(folder,file)      #file converted to d190506e.txt
    getSaleRecords(folder,file)     #file converted to d190506es.txt
    getTransactions(folder,file)
    



        